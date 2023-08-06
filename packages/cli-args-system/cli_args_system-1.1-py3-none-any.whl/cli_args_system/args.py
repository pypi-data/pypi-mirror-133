from sys import argv
from copy import deepcopy
from json import dumps
from typing import Any, Union

from cli_args_system.extras import format_args, get_flags, cast_list
from cli_args_system.flags_content import FlagsContent
from cli_args_system.list_args import ListArgs


class Args(ListArgs):

    def __init__(self, consider_first=False, flags_case_sensitive=False, args_case_sensitive=True, convert_numbers=True,
                 flag_identifier='-', infinity_identifier=True, args=None) -> None:
        """consider_first: if is to consider the first argv element,
        if false, argv[0] will be removed\n
        flags_case_sensitive: if false, all flags will be lowercase \n
        convert_numbers: if True, it will convert in float or int all
        found numbers in argv\n
        flag_identifier: the char that is used to identifies a flag, ex:
        in "--a", the flag_identifier is "-"\n
        infinity_identifier: if false, just the first char will be considered
        as the flag identifier\n
        """
        super().__init__()
        if args is None:
            args = deepcopy(argv)
        self._args = format_args(
            args=args,
            consider_first=consider_first,
            case_sensitive=args_case_sensitive,
            convert_numbers=convert_numbers
        )
        
        
        self._flags = get_flags(
            args=self._args,
            flag_identifier=flag_identifier,
            case_sensitive=flags_case_sensitive,
            infinity_identifier=infinity_identifier
        )
        self._unused_flags = deepcopy(self._flags)


    def args(self) ->list:
        """returns the arguments passed in argv, 
        formatted according to the initial arguments of the class"""
        return deepcopy(self._args)

    
    def flags_dict(self)->dict:
        """returns a dictionary of flags captured in argv"""
        return  deepcopy(self._flags) 


    def flags_names(self,include_default=False) ->list:
        """returns the name of the flags passed in argv\n
        include_default: if False, the default flags will not
        be included on list
        """
        flags = list(self._flags.keys())
        return flags if include_default else flags[1::]


    def total_flags(self,include_default=False) ->int:
        """returns the total size of flags\n
        include_default: if False, the default flags will not
        be included on list"""
        return len(self.flags_names(include_default))


    def unused_flags(self)->dict:
        """returns the flags that were not used after 
        all the flags_content were called
        """
        return  deepcopy(self._unused_flags) 


    def unused_flags_names(self,include_default=False)->list:
        """returns the flags names that were not used after 
        all the flags_content were called\n
        include_default: if False, the default flags will not
        be included on list"""
        flags = list(self._unused_flags.keys())
        return flags if include_default else flags[1::]


    def total_unused_flags(self,include_default=False)->int:
        """returns the total size of flags that were not used after 
        all the flags_content were called\n
        include_default: if False, the default flags will not
        be included on list"""
        return len(self.unused_flags_names(include_default))

    def flag_str(self, *flags)->Union[str,int,None]:
        """return the first founded flag it can be str or int \n
        if does not find any flag, it will return None\n
        flags: the flags that you want to find
        """
        # generate a patronized list of flags
        flags_list = cast_list(*flags)

        for flag in flags_list:
            if flag.__class__ != str:
                raise TypeError('only str are valid for flags')
            try:
                return self._flags[flag][0]
            except (KeyError,IndexError): pass 
        return None 


    def flags_content(self, *flags) -> FlagsContent:
        """returns a FlagsContent object, witch is a group of
        the found flags in argv\n
        flags: the flags that you want to find,
        you can pass a list, tuple, or str"""

        # generate a patronized list of flags
        flags_list = cast_list(*flags)

        # create the filtered args list that will be used
        # to insert the found flags content
        filtered_args = []

        at_least_one_flag_exist = False

        # loop into the flags lis
        for flag in flags_list:
            if flag.__class__ != str:
                raise TypeError('only str are valid for flags')
            try:
                # try to insert into the filtered list
                filtered_args += self._flags[flag]
                # if pass till here, means this flag were inserted in
                # the filtered args
                self._unused_flags.pop(flag)
                at_least_one_flag_exist = True
            except KeyError:
                pass

        # if at least one flag were found, returns FlagsContent object with
        # filtered args
        if at_least_one_flag_exist:
            return FlagsContent(content=filtered_args)
        else:
            # otherwise returns FlagsContent , with None as content
            return FlagsContent(content=None)

    def __eq__(self, o: Any) -> bool:
        """this methods is called when == is used"""
        #if is a dict compare with flags
        if isinstance(o,dict):
            return o == self._flags
        else:
            return super().__eq__(o)

        

        return False

    def __repr__(self) -> str:
        """returns a json representation of the flags attribute"""
        return dumps(self._flags, indent=4)
