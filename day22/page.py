from django.utils.safestring import mark_safe
class Page():
    def __init__(self,current_page,data_count,per_num=10,display_a_num=7,):
        self.current_page = current_page
        self.data_count = data_count
        self.per_num = per_num
        self.display_a_num = display_a_num
    @property
    def count(self):
        count, y = divmod(self.data_count, self.per_num)  ###每页显示10条的话，需要多少页；count是总页数
        if y != 0:  ###如果余数不为0，说明上面计算的总页数无法显示完数据，因此总页数+1显示剩下的
            count += 1
        return count
    @property
    def start(self):
        return (self.current_page-1) * self.per_num
    @property
    def end(self):
        return self.current_page * self.per_num
    def page_str(self):
        page_str = []
        # print(self.current_page,self.display_a_num,self.count)
        if self.current_page <= self.display_a_num:
            '''2个大逻辑判断4个小逻辑判断：
                1：当当前页小于分页a标签个数时，
                    a、当当前页小于分页a标签个数一半时，分页从1开始，分页显示条数+1=总页数，并设为最后一页；
                    b、否则，分页起始页和结束页动态进行计算'''
            if self.current_page <= (self.display_a_num + 1) / 2:
                start1 = 1
                end1 = self.display_a_num
            else:
                start1 = self.current_page - (self.display_a_num - 1) / 2
                end1 = self.current_page + (self.display_a_num - 1) / 2
            '''2：当当前页大于分页a标签个数时：
                a、当当前页+分页a标签个数的一半的和小于总页数，分页起始页和结束页动态进行计算;
                b、否则，起始页为总页数减去分页显示条数+1，结束页为总页数
                '''
        elif self.current_page > self.display_a_num:
            # print('进入大于')
            if self.current_page + (self.display_a_num - 1) / 2 < self.count:
                # print('step 1')
                start1 = self.current_page - (self.display_a_num - 1) / 2
                end1 = self.current_page + (self.display_a_num - 1) / 2
            else:
                # print('step 2')
                start1 = self.count - self.display_a_num + 1
                end1 = self.count
        first_str = "<a class='base active' href='?p=1'>首页</a>"
        page_str.append(first_str)
        if self.current_page == 1:
            prev_str = "<a class='base' href='?p=%s'>上一页</a>" % str(self.current_page)
        else:
            prev_str = "<a class='base' href='?p=%s'>上一页</a>" % str(self.current_page - 1)
        page_str.append(prev_str)
        for i in range(int(start1), int(end1 + 1)):  ###通过获取start1和end1生成分页a标签
            if i == self.current_page:
                comment_str = "<a class='base active' href='?p=%s'>%s</a>" % (i, i)
            else:
                comment_str = "<a class='base' href='?p=%s'>%s</a>" % (i, i)
            page_str.append(comment_str)  ###将分页标签字符串加入列表
        if self.current_page == self.count:
            next_str = "<a class='base' href='?p=%s'>下一页</a>" % str(self.current_page)
        else:
            next_str = "<a class='base' href='?p=%s'>下一页</a>" % str(self.current_page + 1)
        page_str.append(next_str)
        last_str = "<a class='base active' href='?p=%s'>尾页</a>" % str(self.count)
        page_str.append(last_str)
        page_str = "".join(page_str)  ###将所有分页标签的列表转换为字符串
        page_str = mark_safe(page_str)  ### 因为django所有的代码都不能直接显示，如果想要显示，可以通过make_safe将分页标签字符串设置为安全
        return page_str
