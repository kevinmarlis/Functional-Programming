import Data.Maybe

myfMap :: Functor f => (a -> b) -> f a -> f b
myfMap f a = f a
