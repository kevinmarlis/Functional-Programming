-- Note: this isn't runnable code, just notetaking with syntax highlighting.

-- Sum is a function of the Foldable type class.
-- :info sum:
class Foldable (t :: * -> *) where
  ...
  sum :: Num a => t a -> a
  ...

-- From the source:
sum :: (Foldable t, Num a) => t a -> a
sum = getSum . foldMap Sum


newtype Sum a = Sum { getSum :: a }
-- newtype is like data but the type has exactly one constructor with exactly one field inside it.
-- curly braces are for "record syntax", allows field names
        deriving ( Eq       -- ^ @since 2.01
                 , Ord      -- ^ @since 2.01
                 , Read     -- ^ @since 2.01
                 , Show     -- ^ @since 2.01
                 , Bounded  -- ^ @since 2.01
                 , Generic  -- ^ @since 4.7.0.0
                 , Generic1 -- ^ @since 4.7.0.0
                 , Num      -- ^ @since 4.7.0.0
                 )

-- There are some special cases that override the default implementation

-- The implementation for a pair (tuple of two elements) does this:
instance Foldable ((,) a) where
    foldMap f (_, y) = f y
    foldr f z (_, y) = f y z

-- via stackoverflow, 2-tuples are not considered a container of two elements,
-- but a container of one element accompanied by some context. So instance
-- Foldable ((,) a) says that you can extract type a from the pair where type a
-- is the type of the second element of the pair.

-- There isn't an implementation for tuples of more than 2 elements, which is why
-- calling sum on them fails.
