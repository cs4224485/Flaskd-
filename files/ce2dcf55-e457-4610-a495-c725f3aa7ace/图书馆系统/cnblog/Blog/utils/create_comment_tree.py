# Author: harry.cai
# DATE: 2018/7/6

#
# def tree(comment_list):
#     ret = []
#     for row in comment_list:
#         if not row['parent_comment_id']:
#             row['children'] = []
#             ret.append(row)
#         else:
#             recursion(ret, row)
#     return ret
#
#
# def recursion(ret, row):
#     for rt in ret:
#         if rt['nid'] == row['parent_comment_id']:
#             row['children'] = []
#             rt['children'].append(row)
#             return ret
#         else:
#             recursion(rt['children'], row)
