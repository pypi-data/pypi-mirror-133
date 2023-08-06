from copy import deepcopy
from typing import Union
from cli_args_system.list_args import ListArgs


# The Flags Content Extends ListArgs, witch is a "only-read" list
class FlagsContent(ListArgs):
    
    def __init__(self, content: Union[None, list]) -> None:
        """content:the group of args that were found \n"""

        super().__init__()
        # set the exist and filled to false
        self._exist = False
        self._filled = False
        # if content is not None, means the flag exist
        if content is not None:
            self._exist = True
            # if content is not [], means its filled
            if content:
                self._filled = True
                # set the args to content, for to be
            # used with the super(ListArgs)
            self._args = content


    def flags(self)->list:
        """returns The founded flags"""
        return deepcopy(self._args) 


    def exist(self)->bool:
        """returns True if flag were passed on argv else False"""
        return self._exist
    
    def exist_and_empty(self)->bool:
        """returns True if exist and is not filled"""
        return True if self._exist and not self._filled else False 

    def filled(self)->bool:
        """returns True if flag is filled else False, ex: \n
        flags = [a.txt, b.txt ]-> True \n
        flags = [] -> False""" 
        return self._filled
    
    def __repr__(self) -> str:
        return f'exist:  {self._exist}\n'\
               f'filled: {self._filled}\n'\
               f'args:   {self._args}' 
                