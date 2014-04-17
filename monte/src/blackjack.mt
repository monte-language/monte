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
