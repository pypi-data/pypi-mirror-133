import datetime

# 发放积分
# 锁定积分
# 消耗积分
# 回退积分
# 回收积分
# 查询记录
# Create your views here.
from hhycommon.AuthCheck import AuthCheck

from vcoin.models import VCoinModel, VCoinConfigModel, VCoinHistory

class VCoinManager(object):

    # 发放积分
    @staticmethod
    def provideCoin(user_token, coin_count, coin_type):
        try:
            (uid, timestmp) = AuthCheck.checkToken(utoken=user_token)
            print(uid, coin_count, timestmp, user_token)
            # 先查该用户是否有这个类型的积分，没有则报错，否则从锁定的积分中扣除
            vcoin = VCoinModel.objects.filter(uid=uid, vc_config__v_type=coin_type).first()
            if vcoin:
                # saveCoinForUser 缓存用户这一天获得币数
                if VCoinModel.saveCoinForUser(uid=uid, vcoin=vcoin, pre_coin_count=coin_count, coin_type=coin_type):
                    vcoin.v_pre_count += coin_count
                    vcoin.modify_datetime = datetime.datetime.now()
                    vcoin.save()
                    VCoinHistory.saveHistory(uid, coin_count, coin_type, 'provideCoin 预币奖励成功')
                else:
                    VCoinHistory.saveHistory(uid, coin_count, coin_type, '今日已领取最大限量，24小时后再来哦~')
                    raise Exception('今日已领取最大限量，24小时后再来哦~')
            else:
                # 积分类型是管理后台预设的，如果没有则报错
                vcoinConfig = VCoinConfigModel.objects.filter(v_type=coin_type).first()
                if vcoinConfig:
                    vcoin = VCoinModel()
                    vcoin.uid = uid
                    vcoin.expired_datetime = datetime.datetime(2048, 1, 1, 0, 0, 0)
                    vcoin.v_pre_count = coin_count
                    vcoinConfig.v_type = coin_type
                    vcoin.vc_config = vcoinConfig
                    vcoin.save()
                    VCoinHistory.saveHistory(uid, coin_count, coin_type, 'provideCoin 第一次获取预币奖励成功')
                else:
                    VCoinHistory.saveHistory(uid, coin_count, coin_type, 'provideCoin 获取预设配置失败')
                    raise Exception('c类型错误')
        except Exception as e:
            VCoinHistory.saveHistory(uid, coin_count, coin_type, e.__str__())
            print(e)

    # 锁定积分(个人积分转到freeze锁定）买卖积分、商品交易场景，进行中
    @staticmethod
    def freezeCoin(user_token, coin_count, coin_type):
        (uid, vcoin) = VCoinManager.checkVCoin(user_token, coin_count, coin_type)

        minus_coin_count = vcoin.v_count - coin_count
        if minus_coin_count < 0:
            # 积分不够扣的
            VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_count 不够')
            raise Exception('c not enough')

        vcoin.v_count = minus_coin_count
        vcoin.v_freeze_count += coin_count
        vcoin.modify_datetime = datetime.datetime.now()
        vcoin.save()
        VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_count -> v_freeze_count锁定成功')
        return True

    # 消耗积分: 买卖积分、商品交易场景，已完成流程，积分开始消耗
    @staticmethod
    def consumeCoin(user_token, coin_count, coin_type):
        (uid, vcoin) = VCoinManager.checkVCoin(user_token, coin_count, coin_type)

        minus_coin_count = vcoin.v_freeze_count - coin_count
        if minus_coin_count < 0:
            # 积分不够扣的
            VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_freeze_count 不够')
            raise Exception('c not enough')

        vcoin.v_freeze_count = minus_coin_count
        vcoin.modify_datetime = datetime.datetime.now()
        vcoin.save()
        VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_freeze_count消耗掉')
        return True

    # 回退积分，退货之后积分退还
    @staticmethod
    def rollbackCoin(user_token, coin_count, coin_type):
        (uid, vcoin) = VCoinManager.checkVCoin(user_token, coin_count, coin_type)

        minus_coin_count = vcoin.v_freeze_count - coin_count
        if minus_coin_count < 0:
            # 积分不够反的，异常情况？
            VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_freeze_count 不够')
            raise Exception('cfree not enough')
        # 冻结里的积分回退到资产中
        vcoin.v_count += coin_count
        vcoin.v_freeze_count -= coin_count
        vcoin.modify_datetime = datetime.datetime.now()
        vcoin.save()
        VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_freeze_count -> coin_count 回退积分')
        return True

    # 回收积分:从预发积分中扣除，有违规操作，奖励回收
    @staticmethod
    def recycleCoin(user_token, coin_count, coin_type):
        (uid, vcoin) = VCoinManager.checkVCoin(user_token, coin_count, coin_type)

        minus_coin_count = vcoin.v_pre_count - coin_count
        if minus_coin_count < 0:
            # 积分不够扣除的，异常情况？
            VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_pre_count 不够')
            raise Exception('pre not enough')
        # 冻结里的积分回退到资产中
        vcoin.v_pre_count = minus_coin_count
        vcoin.modify_datetime = datetime.datetime.now()
        vcoin.save()
        VCoinHistory.saveHistory(uid, coin_count, coin_type, 'v_pre_count 奖励回收')
        return True

    @staticmethod
    def checkVCoin(user_token, coin_count, coin_type):
        (uid, timestmp) = AuthCheck.checkToken(utoken=user_token)
        print(uid, coin_count, timestmp, user_token)
        # 先查该用户是否有这个类型的积分，没有则报错，否则从锁定的积分中扣除
        vcoin = VCoinModel.objects.filter(uid=uid, vc_config__v_type=coin_type).first()
        if not vcoin:
            VCoinHistory.saveHistory(uid, coin_count, coin_type, '没有币')
            raise Exception('vc not found')
        return (uid, vcoin)

    # 查询记录
    def queryCoinRecord(self, user_token, coin_type=0):
        pass
