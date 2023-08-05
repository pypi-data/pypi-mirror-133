from pprint import pprint
import inspect
import heapq
# 参考 https://docs.python.org/3/library/typing.html#typing.Generator
from typing import Dict, Any, List, Tuple, Generator, Union
import random


def get_func_para(func, del_para=None, add_para: dict = None):
    """提取函数的参数和默认值, 没有默认值设为 None
    比如可以用于设定 TaskDB.result 的例子

    Args:
        func (list, function): 单/多个函数组成的列表, 后面函数出现一样的参数会覆盖前面的默认值
        del_para (set, list, optional): 删除不想看到返回的参数
        add_para (dict, optional): 增加想补充的参数和值, 会覆盖原始值, 不会被 del_para 删除

    Returns:
        dict: 所有函数修剪后的参数和默认值
    """
    paras = {}
    func = func if isinstance(func, list) else [func]
    del_para = set(del_para) if del_para else set()
    add_para = add_para if add_para else {}
    for f in func:
        fullargspec = inspect.getfullargspec(f)
        defaults = fullargspec.defaults if fullargspec.defaults else []
        defaults = [None] * (len(fullargspec.args) - len(defaults)) + list(defaults)
        paras.update({k: v for k, v in zip(fullargspec.args, defaults) if k not in del_para})
    paras.update(add_para)
    return paras


def cover_dict(new_para: dict, default_para: dict, allow_new=False):
    """使用 new_para 中的健值对递归覆盖 default_para 中的值, 遇到非 dict 就不再递归而直接覆盖, 出现类型不一样也会直接覆盖
    比如可以用于新参数覆盖旧参数 (注意因为失误导致的参数覆盖)

    Args:
        new_para (dict): 
        default_para (dict): 被覆盖的, 注意还需要原来的值就要 copy.deepcopy(default_para)
        allow_new (bool): 是否能 让 new_para 出现 default_para 中没有的 key, 能的话就直接加入 default_para

    Returns:
        dict: default_para
    """
    for k, v in new_para.items():
        if k not in default_para:
            if not allow_new:
                raise f'构建了默认参数中没有的参数: {k} not in {set(default_para)}'
            else:
                default_para[k] = v
            continue
        if isinstance(v, dict) and isinstance(default_para[k], dict):
            cover_dict(v, default_para[k])
        else:
            default_para[k] = v
    return default_para


def get(key, obj, default=None):
    """
    递归从dict/list/tuple中取值, 以list的形式，以避免中括号取值数量不灵活的问题
    :param key: list/tuple/int/str; list表示递归取值
    :param obj: dict/list/tuple
    :param default: 寻找不到后返回的默认值
    :return:
    """
    key = key if isinstance(key, list) else [key]
    if len(key) == 0:
        return default
    for i in key:
        try:
            obj = obj[i]
        except:
            obj = default
            break
    return obj


def merge_dict(dict_L: List[Dict], union=True, new_dict=None):
    """递归求多个字典的并/交集, 多个字典的v类型不一样会使用第1个 dict 的值, 如果不存在或为None则优先向后取

    Args:
        dict_L (List[Dict]):
        union (bool): 是否求并集, 否则交集
        new_dict (dict, optional): 递归专用, 不能赋值

    Returns:
        dict: new_dict
    """
    new_dict = {} if new_dict is None else new_dict
    if union:
        set_key = set().union(*dict_L)
    else:
        set_key = set(dict_L[0]).intersection(*dict_L[1:])
    for k in set_key:
        v_L = [d.get(k) for d in dict_L]
        if set(type(v) for v in v_L) == {dict}:
            merge_dict(v_L, union=union, new_dict=new_dict.setdefault(k, {}))
        else:
            new_dict[k] = v_L[0]
            for v in v_L:
                if v is not None:
                    new_dict[k] = v
                    break
    return new_dict


def opt_value_dict(dict1, dict2, opt=lambda v1, v2: v1-v2, new_dict=None):
    """递归求2个字典值的操作值结果, opt操作没有异常才有结果
    如果递归后的 dict1 和 dict2 有一个类型是dict另一个不是, 那么会将是dict的递归然后全部和另一个不是的求opt
    这里的 opt 默认计算的是 dict1 - dict2

    Args:
        dict1 (dict, Any): 
        dict2 (dict, Any): 
        opt (dict, function): 输入 (v1, v2) 返回 计算结果. 如果是 dict 就和 dict1/dict2 一起递归到 非dict(function)
        new_dict (dict, optional): 递归专用, 不能赋值

    Returns:
        dict: new_dict
    """
    new_dict = {} if new_dict is None else new_dict
    for k in (set(dict1) if isinstance(dict1, dict) else set()) | (set(dict2) if isinstance(dict2, dict) else set()):
        v1 = dict1.get(k) if isinstance(dict1, dict) else dict1
        v2 = dict2.get(k) if isinstance(dict2, dict) else dict2
        if type(v1) == dict or type(v2) == dict:
            opt_value_dict(v1, v2, opt[k] if isinstance(opt, dict) else opt, new_dict=new_dict.setdefault(k, {}))
        else:
            try:
                new_dict[k] = opt(v1, v2)
            except:
                ...
    return new_dict


def any_value_dict(dict1, opt=lambda v1, v2: v1 and v2, start_v=True):
    """深度遍历递归求1个字典内部相邻值的操作值结果, opt操作没有异常才更新结果
    这里的 opt 默认计算的是 dict1 中的所有值是不是都是 True

    Args:
        dict1 (dict): 
        opt (dict, function): 输入 (start_v, v) 返回 计算结果. 如果是 dict 就和 dict1 一起递归到 非dict(function)
            v 依次是深度遍历递归的值
        start_v (Any): 初始值, 后面每次更新它

    Returns:
        Any: start_v
    """
    for k, v in dict1.items():
        if type(v) == dict:
            start_v = any_value_dict(v, opt[k] if isinstance(opt, dict) else opt, start_v=start_v)
        else:
            try:
                start_v = opt(start_v, v)
            except:
                ...
    return start_v


def arg_extreme_dict(d: Dict[Any, Dict], dv_key=None, dv_reverse=True, allow_type=None, ban_type=None, traverse_d=None,
                     result=None, root=None):
    """给d中的每个v排序, v中递归的每个元素都排序(只取最大值或最小值), 排序结果的极值用d的k表示
    d中的每个v会取并集key计算, 如果一个dv没有相应的key或为None就不参与极值获取

    Args:
        d (Dict[Any, Dict]): 双层字典, 第二层的每个字典构造格式保持一致, 只允许值不一样或者不存在某些key
        dv_key (dict, function, optional): d中v的每个值使用的排序function, 输入是 (d的k,递归后v值) 对, 输出可排序值
            输入 function 类型就是统一针对所有v的方法
        dv_reverse (dict, bool, optional): d中v的每个值取最大值还是最小值, 默认都是True最大值, 使用dict可针对每个v值选择顺序(不在dict中的还是默认值)
        allow_type (set, list, optional): d中v中的值允许排序的类型, 默认见代码
        ban_type (set, list, optional): d中v中的值不允许排序的类型, 使用这个 allow_type 会失效. 使用时建议加入 dict
        traverse_d (dict, optional): 默认是d中所有v的并集, 用于确定排序对象有哪些k
        result (dict, optional): 用于递归存储结果, 不可以赋值
        root (list, optional): 用于递归存储路径, 不可以赋值

    Returns:
        dict: result
    """
    allow_type = {int, float} if allow_type is None else set(allow_type)
    ban_type = {} if ban_type is None else set(ban_type)
    result = {} if result is None else result
    root = [] if root is None else root
    traverse_d = merge_dict(list(d.values())) if traverse_d is None else traverse_d  # 默认排序对象
    for k, v in traverse_d.items():
        result[k] = {}
        type_v = type(v)
        if (len(ban_type) == 0 and type_v not in allow_type) or (len(ban_type) > 0 and type_v in ban_type):  # 不是允许的类型
            if type_v is dict:  # 是dict就递归
                arg_extreme_dict(d, dv_key=dv_key, dv_reverse=dv_reverse, allow_type=allow_type, ban_type=ban_type,
                                 traverse_d=traverse_d[k], result=result[k], root=root + [k])
        else:
            root_ = root + [k]
            key = dv_key if inspect.isfunction(dv_key) else get(root_, dv_key, lambda t: t[1])  # 排序方式
            reverse = dv_reverse if isinstance(dv_reverse, bool) else get(root_, dv_reverse, True)  # 最大还是最小值排序
            sort_ = heapq.nlargest if reverse else heapq.nsmallest
            result[k] = sort_(1, [(k1, get(root_, v1))  # 出现错误 IndexError: list index out of range 可能是因为加入了排序不了的类型, 比如 None
                              for k1, v1 in d.items() if get(root_, v1) is not None], key=key)[0][0]
    return result


def dict_to_pair(dict1: dict, root=None) -> Generator[Tuple[List, Any], None, None]:
    """深度遍历递归返回所有(k_L,v)对

    Args:
        dict1 (dict): 
        root (list, optional): 用于递归存储路径, 不可以赋值

    Yields:
        Generator[Tuple[List, Any], None, None]: ([k,..],value),..
    """
    root = [] if root is None else root
    for k, v in dict1.items():
        if type(v) == dict:
            yield from dict_to_pair(v, root=root + [k])
        else:
            yield (root + [k], v)


def pair_to_dict(traversed_pair: List[Tuple[List, Any]]) -> dict:
    """所有(k_L,v)对依次还原为dict

    Args:
        traversed_pair (List[Tuple[List, Any]]): ([k,..],value),..

    Returns:
        dict: dict1
    """
    dict1 = {}
    for k_L, v in traversed_pair:
        d = dict1
        for k in k_L[:-1]:
            d = d.setdefault(k, {})
        d[k_L[-1]] = v
    return dict1


if __name__ == '__main__':
    class c:
        def __init__(self) -> None:
            pass

        @staticmethod
        def f(a, b=2, c=3, **kw):
            pass
    # get_func_para
    print('=' * 10, 'get_func_para')
    print(get_func_para(c), get_func_para(c.f))
    print()

    # cover_dict
    print('=' * 10, 'cover_dict')
    new_para = {'a': [1, 2, {'bb': 2}], 'b': {'c': (1, 2), 'd': 2}}
    default_para = {'a': [4, 2, {'b': 21}], 'b': {'c': (1, 1), 'd': 22, 'e': None}}
    pprint(cover_dict(new_para, default_para))
    new_para['dd'] = {12}
    print('allow_new:', cover_dict(new_para, default_para, allow_new=True))
    print()

    # arg_extreme_dict
    print('=' * 10, 'arg_extreme_dict')
    epoch = {
        str(i): {
            i2: {
                i3: random.randint(1, 100) for i3 in ['P', 'R', 'F1']
            } for i2 in ['train', 'dev', 'test']
        } for i in range(5)
    }
    epoch['5'] = {'train': {'P': 30, 'A': 1}}
    epoch = {
        '0': {'dev': {'evaluate': None},
              'test': {'evaluate': {'MAP': 0.11008076900138042,
                                    'NDCG': 0.23014383925192927,
                                    'bpref': 0.5968450000000048,
                                    'macro-F1': 0.10884098853570322,
                                    'macro-P': 0.20855,
                                    'macro-R': 0.07363544070065223}},
              'train': {'evaluate': {'MAP': 0,
                                     'NDCG': 0,
                                     'bpref': 0,
                                     'macro-F1': 0,
                                     'macro-P': 0,
                                     'macro-R': 0},
                        'model': {'acc': 0, 'loss': 1e+38}}},
        '1': {'train': {'model': {'acc': 0.9903333136013576,
                                  'loss': 2.2860701941308523}}}
    }
    print('原始值:')
    pprint(epoch)
    print('极值:')
    pprint(arg_extreme_dict(epoch, dv_reverse=True, ban_type=[dict, type(None)], dv_key=lambda t: -t[1]))
    print()

    # merge_dict / opt_value_dict / any_value_dict
    print('=' * 10, 'merge_dict / opt_value_dict / any_value_dict')
    dict1 = {1: {1: None, 3: 4, 5: 7, 9: 9}, 2: [1, 2], 3: 10}
    dict2 = {1: {1: 2, 3: None, 5: 6, 6: 6}, 3: {4: 1, 5: 2}}
    print('union_dict:', merge_dict([dict1, dict2, dict2]))
    print('intersection_dict:', merge_dict([dict1, dict2, dict2], False))
    ret = opt_value_dict(opt_value_dict(dict1, dict2), None, opt=lambda v1, v2: v1 > 4)
    print('opt_value_dict:', ret)
    print('any_value_dict:', any_value_dict(ret))
    print()

    # dict_to_pair / pair_to_dict
    print('=' * 10, 'dict_to_pair / pair_to_dict')
    print('dict_to_pair:', list(dict_to_pair(dict1)))
    print('pair_to_dict:', pair_to_dict(dict_to_pair(dict1)))
    print()
