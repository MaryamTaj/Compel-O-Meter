import spacy
from spacy import displacy
from typing import Any, Optional


# COPIED FROM LECTURE

class ParseTree:
    """A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The word and its corresponding descriptors stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree, which is empty when self._root is None or when self._root has not subtrees.
    _root: Optional[Any]
    _subtrees: list  # list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list) -> None:  # list[Tree]
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def convert_subtrees(self, subtrees) -> Optional[Any]:
        """
        ...
        """
        if subtrees == []:
            return ParseTree(None, [])
        else:
            for i in range(0, len(subtrees)):
                if subtrees[i][0][2] == self._root[0]:
                    root = subtrees[i][0]
                    new_tree = ParseTree(root, [])
                    self._subtrees.append(new_tree)
                    new_tree.convert_subtrees(subtrees[i][1])

    def check_tag(self, tag) -> list[tuple]:
        negs = []
        if self._root[1] == tag:
            negs.append(self._root)
        for subtree in self._subtrees:
            rec = subtree.check_tag(tag)
            if rec is not None:
                negs.extend(rec)
        return negs


def tree_from_sentence(sentence: str) -> Optional[ParseTree]:
    """Return a parse tree for the given sentence.
    Preconditions:
    - the root word is always dependent on itself. # TODO: Change
    """
    tree_list = tree_list_from_sentence(sentence)
    root_word = find_root(tree_list)
    tree_as_list = tree_from_word(root_word, tree_list, root_word)  # the root is listed to be dependent on itself.
    root = tree_as_list[0]
    subtrees = tree_as_list[1:][0]
    tree = ParseTree(root, [])
    tree.convert_subtrees(subtrees)
    return tree


# def get_depth(nested_list: list) -> int:
#     """Return the depth of the given nested list.
#     >>> get_depth([1, [2, [3, [4, [5]]]]])
#     5
#     """
#     # FIXME: Wrong!!
#     depth = 0
#     if not isinstance(nested_list, list):
#         return depth
#     else:
#         max_depth = 0
#         for sublist in nested_list:
#             if get_depth(sublist) > max_depth:
#                 max_depth = get_depth(sublist)
#             return get_depth(sublist) + 1


def tree_list_from_sentence(sentence: str) -> list[list[tuple[str, str, str, str]]]:
    """Create a tree list for a given sentence.
    >>> tree_list_from_sentence("She drove the Greek piano")
    [[('She', 'nsubj', 'drove', 'PRON'), []], [('drove', 'ROOT', 'drove', 'VERB'), ['She', 'piano']], [('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []], [('piano', 'dobj', 'drove', 'NOUN'), ['the', 'Greek']]]
    """
    spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(sentence)

    tree_list = []

    for token in doc:
        tree_list.append([(token.text,
                           token.dep_,
                           token.head.text,
                           token.pos_),
                          [str(child) for child in token.children]])

    return tree_list


def find_root(tree_list: list[list[tuple[str, str, str, str]]]) -> str:
    """Find the root value of the given tree list.

    Preconditons:
    - 'ROOT' in [tree[0][1] for tree in tree_list]

    >>> tree_list = tree_list_from_sentence("She drove the Greek piano")
    >>> tree = find_root(tree_list)
    >>> tree
    'drove'
    """
    for tree in tree_list:
        if tree[0][1] == 'ROOT':
            return tree[0][0]


def tree_from_word(word: str, tree_list: list, parent: str) -> list:
    """
    >>> tree_list = [[('She', 'nsubj', 'drove', 'PRON'), []], [('drove', 'ROOT', 'drove', 'VERB'), ['She', 'piano']], [('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []], [('piano', 'dobj', 'drove', 'NOUN'), ['the', 'Greek']]]
    >>> tree = tree_from_word('She', tree_list, 'drove')
    >>> tree
    [('She', 'nsubj', 'drove', 'PRON'), []]
    >>> tree = tree_from_word('piano', tree_list,'drove')
    >>> tree
    [('piano', 'dobj', 'drove', 'NOUN'), [[('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []]]]
    >>> tree = tree_from_word('drove', tree_list,'drove')
    >>> tree
    [('drove', 'ROOT', 'drove', 'VERB'), [[('She', 'nsubj', 'drove', 'PRON'), []], [('piano', 'dobj', 'drove', 'NOUN'), [[('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []]]]]]
    """
    # TODO: Change dependent functions calls on this function.
    for tree in tree_list:
        if tree[0][0] == word and tree[0][2] == parent:
            subtrees = tree[1]
            strings = any(isinstance(subtree, str) for subtree in subtrees)
            if not strings:  # BASE CASE
                return tree
            else:  # RECUSRIVE STEPS
                assert strings
                sub = []
                for word in subtrees:
                    subtree = tree_from_word(word, tree_list, tree[0][0])
                    sub.append(subtree)
                return [tree[0], sub]
