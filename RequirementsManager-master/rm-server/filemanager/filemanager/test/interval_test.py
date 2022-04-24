from interval import Interval,IntervalSet

if __name__ =='__main__':
    data = [(2, 4), (9, 13), (6, 12)]

    i1=Interval.between(1,3)
    i2=Interval.between(2,4)
    i3=Interval.between(7,9)
    r2 = IntervalSet([Interval(30, 50), Interval(60, 200), Interval(1150, 1300)])
    # i4=i1.join(i2)
    # print(i4.lower_bound,i4.upper_bound)
    # if i4.overlaps(i3):
    #     print("yeys")
    # intervals = IntervalSet([Interval(2, 2, lower_closed=True, upper_closed=True), Interval(4, 4, lower_closed=True, upper_closed=True)])
    # for _ in intervals:
    #     print(_.lower_bound,_.upper_bound)