# Author: harry.cai
# DATE: 2018/7/9


class PageClass:
    '''
    自定制分页器
    '''
    def __init__(self, current_page, total_count, base_url, per_page=10):
        self.current_page = current_page
        self.per_page = per_page
        self.total_count = total_count
        self.base_url = base_url

    @property
    def db_start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def db_end(self):
        return self.current_page * self.per_page

    def total_page(self):
        v, a = divmod(self.total_count, self.per_page)
        if a != 0:
            v += 1
        return v

    def str_page(self):
        total_page = self.total_page()
        page_list = []
        if self.current_page == 1:
            page_list.append('<a href="#" class=perv disabled>上一页</a>')
        else:
            page_list.append('<a href="/%s?page=%s" class=perv disable>上一页</a>' % (self.base_url, self.current_page - 1))

        if total_page < 11:
            pager_range_start = 1
            pager_range_end = total_page + 1
        else:
            if self.current_page < 6:
                pager_range_start = 1
                pager_range_end = 12
            else:
                pager_range_start = self.current_page - 5
                pager_range_end = self.current_page + 6
                if pager_range_end > total_page:
                    pager_range_start = self.current_page - 10
                    pager_range_end = total_page + 1

        for i in range(pager_range_start, pager_range_end):
            if i == self.current_page:
                page_list.append('<a href="/%s?page=%s" class=active>%s</a>' % (self.base_url, i, i))
            else:
                page_list.append('<a href="/%s?page=%s">%s</a>' % (self.base_url, i, i))

        if self.current_page == total_page:
            page_list.append('<a href="#" class=next disable>下一页</a>')
        else:
            page_list.append('<a href="/%s?page=%s" class=next>下一页</a>' % (self.base_url, self.current_page + 1))
        page_str = "".join(page_list)

        return page_str
