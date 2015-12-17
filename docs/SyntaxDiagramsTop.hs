module Masque.SyntaxDiagrams where

import Control.Applicative (Applicative(..), Alternative(..),
                            (<$>), (<*), (*>))
import qualified Text.Parsec as P

import Masque.ParseUtil
import Masque.FullSyntax
