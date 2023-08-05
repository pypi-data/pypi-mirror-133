"""Class implementation for the parallel animation value.
"""

import re
from typing import Generic
from typing import List
from typing import Match
from typing import Optional
from typing import TypeVar
from typing import Union

from apysc._animation.animation_base import AnimationBase
from apysc._animation.easing import Easing
from apysc._type.int import Int
from apysc._type.variable_name_interface import VariableNameInterface

_T = TypeVar('_T', bound=VariableNameInterface)


class AnimationParallel(AnimationBase[_T], Generic[_T]):
    """
    The parallel animation setting class.
    """

    _animations: List[AnimationBase]

    def __init__(
            self,
            *,
            target: _T,
            animations: List[AnimationBase],
            duration: Union[int, Int] = 3000,
            delay: Union[int, Int] = 0,
            easing: Easing = Easing.LINEAR) -> None:
        """
        The parallel animation setting class.

        Raises
        ------
        ValueError
            - If the animations's target is not unified.
            - If there are changed `duration`, `delay`, or
                `easing` animation settings in the `animations`
                list.

        Parameters
        ----------
        target : VariableNameInterface
            A target instance of the animation target
            (e.g., `DisplayObject` instance).
        animations : list of AnimationBase
            Target animations (e.g., `AnimationX`, `AnimationFillColor`).
        duration : int or Int, default 3000
            Milliseconds before an animation ends.
        delay : int or Int, default 0
            Milliseconds before an animation starts.
        easing : Easing, default Easing.LINEAR
            Easing setting.
        """
        import apysc as ap
        with ap.DebugInfo(
                callable_='__init__', locals_=locals(),
                module_name=__name__, class_=AnimationParallel):
            from apysc._expression import expression_variables_util
            from apysc._expression import var_names
            variable_name: str = expression_variables_util.\
                get_next_variable_name(type_name=var_names.ANIMATION_PARALLEL)
            self._animations = animations
            self._set_basic_animation_settings(
                target=target,
                duration=duration,
                delay=delay,
                easing=easing)
            super(
                AnimationParallel,
                self).__init__(
                variable_name=variable_name)
            self._validate_animation_targets_are_unified()
            self._validate_animations_duration_are_default_vals()
            self._validate_animations_delay_are_default_vals()
            self._validate_animations_easing_are_default_vals()

    def _validate_animations_easing_are_default_vals(self) -> None:
        """
        Validate whether the animations easing settings are
        default values (not changed).

        Raises
        ------
        ValueError
            If there is an animation target that is changed
            easing setting.
        """
        for animation in self._animations:
            if animation._easing == Easing.LINEAR:
                continue
            err_msg: str = (
                'There is an animation target that is changed '
                f'easing setting: {animation._easing.name}'
                '\nThe easing setting of animation in the `animations` '
                'argument can not be changed.'
                f'\nTarget animation type: {type(animation)}'
            )
            raise ValueError(err_msg)

    def _validate_animations_delay_are_default_vals(self) -> None:
        """
        Validate whether the animations delay settings are
        default values (not changed).

        Raises
        ------
        ValueError
            If there is an animation target that is changed
            delay setting.
        """
        for animation in self._animations:
            if animation._delay._value == 0:
                continue
            err_msg: str = (
                'There is an animation target that is changed '
                f'delay setting: {animation._delay._value}'
                '\nThe delay setting of animation in the `animations`'
                'argument can not be changed.'
                f'\nTarget animation type: {type(animation)}'
            )
            raise ValueError(err_msg)

    def _validate_animations_duration_are_default_vals(self) -> None:
        """
        Validate whether the animations duration settings are
        default values (not changed).

        Raises
        ------
        ValueError
            If there is an animation target that is changed
            duration setting.
        """
        for animation in self._animations:
            if animation._duration._value == 3000:
                continue
            err_msg: str = (
                'There is an animation target that is changed '
                f'duration setting: {animation._duration._value}'
                '\nThe duration setting of animation in the '
                '`animations` argument can not be changed.'
                f'\nTarget animation type: {type(animation)}'
            )
            raise ValueError(err_msg)

    def _validate_animation_targets_are_unified(self) -> None:
        """
        Validate whether the specified animation's targets are unified.

        Raises
        ------
        ValueError
            If the specified animation targets are not unified.
        """
        for animation in self._animations:
            if animation._target == self._target:
                continue
            err_msg: str = (
                'There is not unified animation target instance: '
                f'{animation._target} (type: {type(animation._target)})'
                f'\nExpected instance: {self._target} (type: '
                f'{type(self._target)})'
                f'\nTarget animation type: {type(animation)}'
                f'\nPlease unify the animation targets of the '
                'animation_parallel interface argument.'
            )
            raise ValueError(err_msg)

    def _get_animation_func_expression(self) -> str:
        """
        Get a animation function expression.

        Returns
        -------
        expression : str
            Animation function expression.
        """
        expression: str = ''
        attr_strs: List[str] = []
        for i, animation in enumerate(self._animations):
            single_expression: str = \
                animation._get_animation_func_expression()
            single_expression = single_expression.replace(';', '')
            if '.attr' in single_expression:
                match: Optional[Match] = re.search(
                    pattern=(
                        r'.*\.attr\({(.*?)}\)'
                    ),
                    string=single_expression,
                    flags=re.MULTILINE | re.DOTALL)
                if match is not None:
                    attr_strs.append(match.group(1))
            else:
                expression += single_expression
            if i == len(self._animations) - 1:
                expression += self._make_animation_attr_exp(
                    attr_strs=attr_strs)
                expression += ';'
        return expression

    def _make_animation_attr_exp(self, *, attr_strs: List[str]) -> str:
        """
        Make an animation attribute expression string.

        Parameters
        ----------
        attr_strs : list of str
            Target attribute strings.

        Returns
        -------
        expression : str
            Created attribute expression string.
        """
        expression: str = '\n  .attr({'
        for i, attr_str in enumerate(attr_strs):
            expression += f'\n    {attr_str}'
            if i != len(attr_strs) - 1:
                expression += ','
        expression += '\n  })'
        return expression

    def _get_complete_event_in_handler_head_expression(self) -> str:
        """
        Get an expression to be inserted into the complete event
        handler's head.

        Returns
        -------
        expression : str
            An expression to be inserted into the complete event
            handler's head.
        """
        expression: str = ''
        for animation in self._animations:
            if expression != '':
                expression += '\n'
            single_expression: str = animation.\
                _get_complete_event_in_handler_head_expression()
            expression += single_expression
        return expression
