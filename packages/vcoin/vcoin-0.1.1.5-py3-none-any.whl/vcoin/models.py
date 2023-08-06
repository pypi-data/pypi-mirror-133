
from django.core.cache import cache
from django.db import models

class VCoinHistory(models.Model):
    # user_token, coin_count, coin_type
    vchid = models.AutoField(primary_key=True, verbose_name='主键')
    v_count = models.IntegerField(default=0, verbose_name='积分个数')
    v_type = models.IntegerField(default=0, verbose_name='积分类型')
    v_desc = models.CharField(max_length=50, default='desc', verbose_name='操作描述')
    uid = models.CharField(max_length=50, default='', verbose_name='uid')
    create_datetime = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='创建记录的时间')

    def saveHistory(uid, coin_count, coin_type, desc):
        history = VCoinHistory()
        history.uid = uid
        history.v_count = coin_count
        history.v_type = coin_type
        history.v_desc = desc
        history.save()

    class Meta:
        verbose_name_plural = '历史记录'

    def __str__(self):
        return 'uid: %s 积分个数:%s 类型：%s 描述：%s %s' % (self.uid, self.v_count, str(self.v_type), self.v_desc, self.create_datetime)


class VCoinConfigModel(models.Model):
    vcid = models.AutoField(primary_key=True, verbose_name='主键')
    # day_publish_max_count = models.IntegerField(default=10000, verbose_name='日发放积分数')
    day_user_max_count = models.IntegerField(default=70, verbose_name='单日用户日领取数')
    v_type = models.IntegerField(default=0, verbose_name='积分类型')
    v_name = models.CharField(max_length=32, default='积分', verbose_name='积分名称')
    v_exchange_ratio = models.DecimalField(max_digits=10, decimal_places=4, default=10,
                                           verbose_name='兑换比例（1B=10积分）积分/b=10')
    v_status = models.IntegerField(default=0, verbose_name='状态（0生效中 1锁定中 2已失效）,这个状态标记这个积分还要不要用')

    class Meta:
        verbose_name_plural = '积分配置'

    def __str__(self):
        return self.v_name + ' -> 积分类型：' + str(self.v_type)


class VCoinModel(models.Model):
    vid = models.AutoField(primary_key=True, verbose_name='主键')
    uid = models.CharField(max_length=50, default='1', verbose_name='外部用户id')
    expired_datetime = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='过期时间')
    create_datetime = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='创建记录的时间')
    modify_datetime = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='记录变更时间')
    v_count = models.DecimalField(max_digits=10, decimal_places=4, default=0, verbose_name='个人当前type的生效中积分个数')
    v_freeze_count = models.DecimalField(max_digits=10, decimal_places=4, default=0, verbose_name='个人当前type的冻结积分个数')
    v_pre_count = models.DecimalField(max_digits=10, decimal_places=4, default=0, verbose_name='预发积分个数，积分全部走预发')
    vc_config = models.ForeignKey(VCoinConfigModel, on_delete=models.CASCADE, verbose_name='积分配置')

    class Meta:
        verbose_name_plural = '积分模型'
        indexes = [models.Index(fields=['uid']), ]

    def __str__(self):
        count = " 可用积分(%s)" % str(self.v_count)
        fcount = " 冻结：(%s)" % str(self.v_freeze_count)
        pcount = " 预发：(%s)" % str(self.v_pre_count)
        type = " 类型：(%s)" % str(self.vc_config.v_name)
        return count + fcount + pcount + type

    def saveCoinForUser(uid, vcoin, pre_coin_count, coin_type):
        key = '%s-%s' % (uid, coin_type)
        coin_today = cache.get(key, 0)
        print(coin_today)
        coin_sum = int(coin_today) + pre_coin_count
        # 没到限制线，发送奖励
        print(vcoin.vc_config.day_user_max_count)
        print(coin_sum)
        if vcoin.vc_config.day_user_max_count - coin_sum >= 0:
            cache.set(key, coin_sum, timeout=86400)
            return True
        else:
            return False

# 发放积分
# 锁定积分
# 消耗积分
# 回退积分
# 回收积分
# 查询记录
