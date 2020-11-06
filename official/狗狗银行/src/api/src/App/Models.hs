{-# LANGUAGE DerivingStrategies #-}
{-# LANGUAGE GADTs #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE QuasiQuotes #-}
{-# LANGUAGE StandaloneDeriving #-}
{-# LANGUAGE TemplateHaskell #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE UndecidableInstances #-}

module App.Models
    ( Account (..)
    , AccountId
    , EntityField (..)
    , Transaction (..)
    , TransactionId
    , Unique (..)
    , User (..)
    , UserId
    , migrateAll
    ) where

import RIO

import Yesod

import App.Types


share [mkPersist sqlSettings, mkMigrate "migrateAll"] [persistLowerCase|
User
    token Text
    date Date
    nextAccountId AccountIdPerUser
    UniqueUserToken token
Account
    userId UserId
    idPerUser AccountIdPerUser
    data AccountData
    nextTransactionId TransactionIdPerAccount
    UniqueAccountIdPerUser userId idPerUser
Transaction
    userId UserId
    accountIdPerUser AccountIdPerUser
    idPerAccount TransactionIdPerAccount
    date Date
    description Text
    amount Integer
    balance Integer
    UniqueTransactionIdPerAccount userId accountIdPerUser idPerAccount
|]
