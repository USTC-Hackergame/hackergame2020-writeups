{-# OPTIONS_GHC -Wno-unused-top-binds #-}
{-# LANGUAGE QuasiQuotes #-}
{-# LANGUAGE TemplateHaskell #-}
{-# LANGUAGE TypeFamilies #-}

module Main (main) where

import RIO hiding (Handler)
import qualified RIO.Partial as RIO'
import qualified RIO.Text as T

import Control.Monad.Logger (filterLogger, runStderrLoggingT)
import Data.Aeson.Types (Parser, parseMaybe)
import Database.Persist.Sql (ConnectionPool, SqlBackend, runMigration, runSqlPool)
import Database.Persist.Sqlite (withSqlitePool)
import Network.Wai.Handler.Warp (run)
import Network.Wai.Middleware.Cors
    ( CorsResourcePolicy (corsRequestHeaders)
    , cors
    , simpleCorsResourcePolicy
    )
import Yesod

import App.Models
import App.Types


accountLimit :: AccountIdPerUser
accountLimit = 1000

transactionLimit :: TransactionIdPerAccount
transactionLimit = 100000

main :: IO ()
main = runLoggingT $ withSqlitePool "db" 1 $ \pool -> liftIO $ do
    runSqlPool (runMigration migrateAll) pool
    app <- toWaiApp $ Api
        { apiDatabasePool = pool
        }
    run 3000 $ cors getPolicy app
  where
    runLoggingT = runStderrLoggingT . filterLogger (\_ l -> l >= Yesod.LevelInfo)
    getPolicy _ = Just $ simpleCorsResourcePolicy
        { corsRequestHeaders = ["Authorization", "Content-Type"]
        }


data Api = Api
    { apiDatabasePool :: !ConnectionPool
    }

mkYesod "Api" [parseRoutes|
/user UserR GET
/transactions TransactionsR GET
/reset ResetR POST
/create CreateR POST
/eat EatR POST
/transfer TransferR POST
|]

instance Yesod Api where
    makeSessionBackend _ = return Nothing
    yesodMiddleware = id

instance YesodPersist Api where
    type YesodPersistBackend Api = SqlBackend
    runDB action = do
        pool <- getsYesod apiDatabasePool
        runSqlPool action pool


getBody :: FromJSON a => (a -> Parser b) -> ReaderT SqlBackend Handler b
getBody parser = do
    body <- requireCheckJsonBody
    maybe (invalidArgs ["请求解析失败"]) pure $ parseMaybe parser body

getUser :: ReaderT SqlBackend Handler (Entity User)
getUser = do
    token <- lookupBearerAuth >>= maybe notAuthenticated pure
    unless (T.length token > 30) notAuthenticated
    getBy (UniqueUserToken token) >>= \case
        Just x -> pure x
        Nothing -> do
            let ai = minBound
                user = User
                    { userToken = token
                    , userDate = minBound
                    , userNextAccountId = RIO'.succ ai
                    }
            ui <- insert user
            void $ insert $ Account
                { accountUserId = ui
                , accountIdPerUser = ai
                , accountData = mkDebit
                , accountNextTransactionId = minBound
                }
            void $ change (Entity ui user) ai "开户" 1000
            pure (Entity ui user)

change :: Entity User -> AccountIdPerUser -> Text -> Integer -> ReaderT SqlBackend Handler (Entity Account)
change (Entity ui user) ai description delta = do
    Entity accountId account <- getBy (UniqueAccountIdPerUser ui ai)
        >>= maybe (invalidArgs ["卡不存在"]) pure
    let ti = accountNextTransactionId account
    when (ti > transactionLimit) $ invalidArgs ["某张卡的交易数量已达到上限"]
    d <- either (invalidArgs . pure) pure
        $ accountChange delta $ accountData account
    void $ insert $ Transaction
        { transactionUserId = ui
        , transactionAccountIdPerUser = ai
        , transactionIdPerAccount = ti
        , transactionDate = userDate user
        , transactionDescription = description
        , transactionAmount = delta
        , transactionBalance = accountBalance d
        }
    replace accountId $ account { accountData = d, accountNextTransactionId = RIO'.succ ti }
    pure $ Entity accountId account

nextDay :: Entity User -> ReaderT SqlBackend Handler ()
nextDay (Entity ui user) = do
    accounts <- fmap entityVal <$> selectList [AccountUserId ==. ui] []
    forM_ accounts $ \account -> do
        let ai = accountIdPerUser account
            d = accountData account
        change (Entity ui user) ai "利息" $ accountInterest d
    replace ui $ user { userDate = RIO'.succ $ userDate user }

totalValue :: [Entity Account] -> Integer
totalValue = sum . fmap (accountValue . accountData . entityVal)


getUserR :: Handler Value
getUserR = runDB $ do
    Entity ui user <- getUser
    accounts <- selectList [AccountUserId ==. ui] [Asc AccountIdPerUser]
    flag <- if totalValue accounts >= 2000
        then Just <$> makeFlag
        else pure Nothing
    pure $ object
        [ "date" .= userDate user
        , "accounts" .= (accountToJson <$> entityVal <$> accounts)
        , "flag" .= flag
        ]
  where
    makeFlag = pure ("flag{W0W.So.R1ch.Much.Smart.52f2d579}" :: Text)
    accountToJson x = object
        [ "id" .= accountIdPerUser x
        , "type" .= accountType (accountData x)
        , "balance" .= accountBalance (accountData x)
        ]


getTransactionsR :: Handler Value
getTransactionsR = runDB $ do
    ui <- entityKey <$> getUser
    ai <- lookupGetParam "account" >>= \case
        Just x -> maybe (invalidArgs ["参数解析失败"]) pure $ fromPathPiece x
        Nothing -> invalidArgs ["参数不足"]
    transactions <- selectList
        [ TransactionUserId ==. ui
        , TransactionAccountIdPerUser ==. ai
        ]
        [ Asc TransactionIdPerAccount ]
    pure $ object
        [ "transactions" .= (transactionToJson <$> entityVal <$> transactions)
        ]
  where
    transactionToJson x = object
        [ "id" .= transactionIdPerAccount x
        , "date" .= transactionDate x
        , "description" .= transactionDescription x
        , "change" .= transactionAmount x
        , "balance" .= transactionBalance x
        ]


postResetR :: Handler ()
postResetR = runDB $ do
    ui <- entityKey <$> getUser
    deleteWhere [TransactionUserId ==. ui]
    deleteWhere [AccountUserId ==. ui]
    delete ui


postCreateR :: Handler ()
postCreateR = runDB $ do
    Entity ui user <- getUser
    d <- getBody parser
    let ai = userNextAccountId user
    when (ai > accountLimit) $ invalidArgs ["卡数量已达到上限"]
    void $ insert $ Account
        { accountUserId = ui
        , accountIdPerUser = ai
        , accountData = d
        , accountNextTransactionId = minBound
        }
    void $ change (Entity ui user) ai "开户" 0
    replace ui $ user { userNextAccountId = RIO'.succ ai }
  where
    parser x = x .: "type" >>= \case
        "debit" -> pure mkDebit
        "credit" -> pure mkCredit
        (_ :: Text) -> fail "卡类型错误"


postEatR :: Handler ()
postEatR = runDB $ do
    Entity ui user <- getUser
    ai <- getBody parser
    void $ change (Entity ui user) ai "吃饭" (-10)
    nextDay (Entity ui user)
  where
    parser x = x .: "account"


postTransferR :: Handler ()
postTransferR = runDB $ do
    Entity ui user <- getUser
    (aiSrc, aiDst, amount) <- getBody parser
    void $ change (Entity ui user) aiSrc "转账" $ negate amount
    void $ change (Entity ui user) aiDst "转账" amount
  where
    parser x = (,,)
        <$> x .: "src"
        <*> x .: "dst"
        <*> x .: "amount"
