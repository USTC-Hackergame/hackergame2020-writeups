{-# OPTIONS_GHC -Wno-orphans #-}
{-# LANGUAGE TemplateHaskell #-}

module App.Types
    ( AccountData
    , AccountIdPerUser
    , Date
    , TransactionIdPerAccount
    , accountBalance
    , accountChange
    , accountInterest
    , accountType
    , accountValue
    , mkCredit
    , mkDebit
    ) where

import RIO
import qualified RIO.Text as T

import Database.Persist.Sql (PersistFieldSql (sqlType))
import Yesod


instance PersistField Integer where
    toPersistValue = toPersistValue . show
    fromPersistValue x@(PersistText t) = case readMaybe $ T.unpack t of
        Just v -> Right v
        Nothing -> Left $ T.pack $ "Can not read as Integer: " <> show x
    fromPersistValue (PersistInt64 i) = Right $ fromIntegral i
    fromPersistValue x = Left $ T.pack $ "Can not read as Integer: " <> show x

instance PersistFieldSql Integer where
    sqlType _ = SqlString


newtype Date = Date Int64
    deriving stock (Show)
    deriving newtype (Enum, PersistField, PersistFieldSql, ToJSON)

instance Bounded Date where
    minBound = Date 1
    maxBound = Date maxBound


newtype AccountIdPerUser = AccountIdPerUser Int64
    deriving stock (Show)
    deriving newtype (Enum, Eq, FromJSON, Num, Ord, PathPiece, PersistField, PersistFieldSql, ToJSON)

instance Bounded AccountIdPerUser where
    minBound = AccountIdPerUser 1
    maxBound = AccountIdPerUser maxBound


newtype TransactionIdPerAccount = TransactionIdPerAccount Int64
    deriving stock (Show)
    deriving newtype (Enum, Eq, Num, Ord, PersistField, PersistFieldSql, ToJSON)

instance Bounded TransactionIdPerAccount where
    minBound = TransactionIdPerAccount 1
    maxBound = TransactionIdPerAccount maxBound


data AccountData
    = Debit !Integer
    | Credit !Integer
    deriving (Read, Show)
derivePersistField "AccountData"

mkDebit :: AccountData
mkDebit = Debit 0

mkCredit :: AccountData
mkCredit = Credit 0

accountValue :: AccountData -> Integer
accountValue (Debit v) = v
accountValue (Credit v) = -v

accountType :: AccountData -> Text
accountType (Debit _) = "debit"
accountType (Credit _) = "credit"

accountBalance :: AccountData -> Integer
accountBalance (Debit v) = v
accountBalance (Credit v) = v

accountChange :: Integer -> AccountData -> Either Text AccountData
accountChange d (Debit v)
    | v + d >= 0 = Right $ Debit (v + d)
    | otherwise = Left "余额不足"
accountChange d (Credit v)
    | v - d >= 0 = Right $ Credit (v - d)
    | otherwise = Left "还款不能超过欠款额"

accountInterest :: AccountData -> Integer
accountInterest (Debit v) = round $ fromInteger v * (0.003 :: Rational)
accountInterest (Credit 0) = 0
accountInterest (Credit v) = negate $ max 10 $ round $ fromInteger v * (0.005 :: Rational)
