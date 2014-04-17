def makeNIL():
    object NIL():
        to size():
            return 0
        to find(seek, key):
            return null
            # or raise something about the value not being found
        to findPrekeyed(seek, key):
            return null
            # or raise some error

def makeNode(value, left, right, red :Bool):
    return object Node:

        # Oh eww. Silly monte.
        to getL():
            return left
        to getR():
            return right
        to getV():
            return value
        to getB():
            return red 

        to size():
            # Recursively find the size of a tree. Slow.
            return 1 + left.size() + right.size()

        to find(seek, key):
            # Find value 'seek' in a node, using a key function.
            def me := key(value)
            if (key(seek) < me):
                return left.find(seek, key)
            if (key(seek) > me):
                return right.find(seek, key)
            if (key(seek) == me):
                return value

        to findPrekeyed(seek, key):
            def me := key(value)
            if (seek < me):
                return left.findPrekeyed(seek, key)
            if (seek > me):
                return right.findPrekeyed(seek, key)
            if (seek == me):
                return value

        to rotateLeft():

            #     A                  C
            #    / \                / \
            #   B   C      =>      A   E
            #      / \            / \
            #     D   E          B   D
 
            def new := makeNode(value, left, right.getL(), True)
            def top := makeNode(right.getV(), new, right.getR(), red)
            return top

        to rotateRight():

            #      A               B
            #     / \             / \
            #    B   C    =>     D   A
            #   / \                 / \
            #  D   E               E   C

            def new := makeNode(value, left, right.getL(), True)
            def top := makeNode(right.getV(), new, right.getR(), red)
            return top

        to flip():
            # Invert colors of a node and its children
            def l := makeNode(left.getV(), left.getL(), left.getR(), !left.getB())
            def r := makeNode(right.getV(), right.getL(), right.getR(), !right.getB())
            def top := makeNode(value, l, r, !red)
            return top

        to balance():
            # Balance a node. 
            # The balance is inductive and relies on all subtrees being
            # balanced recursively or by construction. If the subtrees are not
            # balanced, this will NOT fix them. 

            var node := Node 

            # Always lean left with red nodes.
            if (right.getR()):
                node := node.rotateLeft()

            # Never permit red nodes to have red children. Note that if the
            # left-hand node is NIL, it will short-circuit and fail this test.

            if (left.getB() && left.getL().getB()):
                node := node.rotateRight()

            # Finally, move red children on both sides up to the next level,
            # reducing the total redness.

            if (left.getB() && right.getB()):
                node := node.flip()

            return node

        to insert(val, key):
            # Insert a value into a tree rooted at the given node, and return
            # whether this was an insertion or update.
 
            # Balances the tree during insertion. 

            # An update is performed instead of an insertion if a value in the
            # tree compares equal to the new value. 

            var node := Node

            # Base case: Insertion into the empty tree is just creating a new
            # node with no children. 
            
            if (node == NIL):
                return [makeNode(val, makeNIL(), makeNIL(), True), True]

            # Recursive case: Insertion into a non-empty tree is insertion is
            # into whichever of the two sides is correctly compared. 

            def keyV := key(val)
            def keyMe := key(value)

            if (keyV < keyMe):
                def [l, insertion] := left.insert(val, key)
                node := makeNode(value, l, right, red)
            else if (keyMe < keyV):
                def [r, insertion] := right.insert(val, key)
                node := makeNode(value, left, r, red)
            else if (keyV == keyMe):
                # Exact hit on this node. Perform an update.
                node := makeNode(val, left, right, red)
                def insertion := False

            # And balance on the way back up.
            return [node.balance(), insertion]

        to moveRedLeft():
            # Shuffle red to the left of a tree
            var node := Node.flip()
            if (node.getR() != NIL && node.getR().getL().getB()):
                node := makeNode(value, left, right.rotateRight())
                node := node.rotateLeft().flip()
            return node

        to moveRedRight():
            # Shuffle red to the right of a tree.
            node := Node.flip()
            if (left != NIL && left.getL().getL().getB()):
                node := node.rotateRight().flip()
            return node

        to deleteMin():
            # Delete the left-most value from a tree

            node := Node

            # Base case: If nobody is smaller than me, delete myself. 
            if (left == NIL):
                return [makeNIL(), value]

            # Acquire more reds if necessary to continue the traversal. The
            # double-deep check is fine because NIL is red.

            if (!left.getB() && !left.getL().getB()):
                 node := node.moveRedLeft()

            # Recursive case: Delete minimum of all less than this

            def [l, val] = left.deleteMin()
            node := makeNode(value, l, right, red)

            return [self.balance(), val]

        to deleteMax():
            # Delete the right-most value from a tree.

            node := Node

            # Attempt to rotate left-leaning reds to the right.
            if (left.getB()):
                node := node.rotateRight()

            # Base case: If there's nothing bigger than me, I go away.
            if (right == NIL):
                return [makeNIL(), value]

            # Acquire more reds if necessary to continue. NIL is red.
            if (!right.getB() && !right.getL().getB()):
                node := node.moveRedRight()

            # Recursive case: Delete max of larger subtree
            def [r, val] :=  right.deleteMax()
            node := makeNode(value, left, r, red)

            return node.balance(), val

        to delete(val, key):
            # Delete a value from a tree.

            var node := Node

            # Base case: The empty tree cannot possibly have the desired value.
            if (node == NIL):
                pass
                # XXX Raise some error, KeyError in the Python implementation

            def toDel := key(val)
            def me := key(value)

            # We lean to the left, so the left case stands alone.
            if (toDel < me):
                if (!left.getB() && left != NIL && !left.getL().getB()):
                    # Delete towards the left
                    def l := left.delete(val, key)
                    node := makeNode(value, l, right, red)
            else:
                # If we lean left, time to lean right
                if (left.getB()):
                    node := node.rotateRight()

                # Best case: The node on our right, which we just put there,
                # is a red link and also we were just holding the node to
                # delete. In that case, we just rotated NIL into our current
                # node, and the node to the right is the lone matching node to
                # delete. (Whatever that's supposed to mean.)

                if (toDel == me && right == NIL):
                    return makeNIL()

                # No? Okay. Move more reds to the right so we can continue to
                # traverse thataways. Here, we do have to confirm that there's
                # no NIL on our right...

                if (!right.getB() && right != NIL && !right.getL().getB()):
                    node := node.moveRedRight()
                if (me < toDel):
                    # Delete toward the right
                    def r := right.delete(val, key)
                    node := makeNode(value, left, r, red)
                else:
                    # Annoying case: The current node was the node to delete
                    # all along! Use right-handed minimum deletion. First find
                    # the replacement value to rebuild the current node with,
                    # then delete the replacement value from the right-side
                    # tree. Finally, create the new node with the old value
                    # replaced and the replaced value deleted.

                    var rt := right
                    while (rt != NIL):
                        rt := rt.getL()
                    def [r, replacement] := node.getR().deleteMin()
                    node := makeNode(replacement, left, r, red)

            return node.balance()
