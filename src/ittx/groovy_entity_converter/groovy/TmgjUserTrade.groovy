package com.ittx.oms.trade.domain.tmgj

import com.ittx.cbt.domain.BaseEntity

import java.time.LocalDateTime

/**
 * 天猫国际账单数据
 */
public class TmgjUserTrade extends BaseEntity {

    static DEFINE = define([
            table        : 'tmgj_user_trade',
            idColumn     : 'id',
            cache        : false,
            cacheKey     : 'tmgj_user_trade',
            autoIncrement: true,
            logHistory   : true
    ])

    @Override
    Object getEntityId() {
        return id
    }

    Integer id // ID
    String storeCode // 店铺编码
    String brandCode // 品牌编码
    String transactionId // 子订单号
    String originalTransactionId // 原订单号
    LocalDateTime paymentTime // 付款时间
    LocalDateTime billingTime // 账单发生时间
    BigDecimal rmbNetvalue // 人民币未税金额
    BigDecimal rmbAmount // 人民币账单金额
    BigDecimal rmbFee // 人民币费用金额
    BigDecimal rmbSettlement // 人民币提现金额
    BigDecimal rmbFeeAmount // 人民币税金
    BigDecimal rate // 汇率
    BigDecimal hkbNetvalue // 港币未税金额
    BigDecimal hkbAmount // 港币账单金额
    BigDecimal hkbFee // 港币费用金额
    BigDecimal hkbSettlement // 港币提现金额
    BigDecimal hkbFeeAmount // 港币税金
    String transactionType // 交易分类
    String returnType // 售后标记
    String fileType // 文件类型

    String sourceOrderCode // 平台订单号
    String classification // 账单分类
    String subjectCode //科目编码
    String subjectName // 科目名称
    String inOutType // 收支方向
    Integer verificationStatus = 0 // 核销状态 0：未收集，1：已收集

    LocalDateTime created // 创建时间 
    String createdBy // 创建人
    LocalDateTime lastUpdated // 更新时间
    String lastUpdatedBy // 更新人
    Integer version // 数据版本
    String userDef1 // 自定义字段1
    String userDef2 // 自定义字段2
    String userDef3 // 自定义字段3
    String userDef4 // 自定义字段4
    String userDef5 // 自定义字段5
    String userDef6 // 自定义字段6
    String userDef7 // 自定义字段7
    String userDef8 // 自定义字段8 已占用：代表SAP凭证生成状态

}
