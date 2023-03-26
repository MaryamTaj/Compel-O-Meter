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
    _subtrees: list # list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list) -> None: # list[Tree]
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def convert_subtrees(self) -> Optional[Any]:
        """
        ...
        """
        ...

def tree_from_sentence(sentence: str) -> Optional[Tree]:
    """Return a parse tree for the given sentence.
    """
    tree_list = tree_list_from_sentence(sentence)
    root_word = find_root(tree_list)
    tree_as_list = tree_from_word(root_word, tree_list)
    root = tree_as_list[0]
    subtrees = tree_as_list[1:]
    depth = get_depth(subtrees)

def get_depth(nested_list: list) -> int:
    """Return the depth of the given nested list.
    >>> get_depth([1, [2, [3, [4, [5]]]]])
    5
    """
    # FIXME: Wrong!!
    depth = 0
    if not isinstance(nested_list, list):
        return depth
    else:
        max_depth = 0
        for sublist in nested_list:
            if get_depth(sublist) > max_depth:
                max_depth = get_depth(sublist)
            return get_depth(sublist) + 1

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

def find_root(tree_list: list[list[tuple[str, str, str, str]]]) -> list:
    """Find the root value of the given tree list.

    Preconditons:
    - 'ROOT' in [tree[0][1] for tree in tree_list]

    >>> tree_list = tree_list_from_sentence("She drove the Greek piano")
    >>> tree = find_root(tree_list)
    'drove'
    """
    for tree in tree_list:
        if tree[0][1] == 'ROOT':
            return tree[0][0]

def tree_from_word(word: str, tree_list: list) -> list:
    """
    >>> tree_list = [[('She', 'nsubj', 'drove', 'PRON'), []], [('drove', 'ROOT', 'drove', 'VERB'), ['She', 'piano']], [('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []], [('piano', 'dobj', 'drove', 'NOUN'), ['the', 'Greek']]]
    >>> tree = tree_from_word('She', tree_list)
    >>> tree
    [('She', 'nsubj', 'drove', 'PRON'), []]
    >>> tree = tree_from_word('piano', tree_list)
    >>> tree
    [('piano', 'dobj', 'drove', 'NOUN'), [[('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []]]]
    >>> tree = tree_from_word('drove', tree_list)
    >>> tree
    [('drove', 'ROOT', 'drove', 'VERB'), [[('She', 'nsubj', 'drove', 'PRON'), []], [('piano', 'dobj', 'drove', 'NOUN'), [[('the', 'det', 'piano', 'DET'), []], [('Greek', 'amod', 'piano', 'ADJ'), []]]]]]
    """
    for tree in tree_list:
        if tree[0][0] == word:
            subtrees = tree[1]
            strings = any(isinstance(subtree, str) for subtree in subtrees)
            if not strings: # BASE CASE
                return tree
            else:
                assert strings
                subtrees = [tree_from_word(word, tree_list) for word in subtrees]
                return [tree[0], subtrees]

