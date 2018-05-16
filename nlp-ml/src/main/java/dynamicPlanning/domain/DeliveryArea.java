package dynamicPlanning.domain;

import dynamicPlanning.Constant;

/**
 * 构建配送范围
 */
public enum DeliveryArea {

    /**
     * 市内配送
     */
    INNER_CITY_DELIVERY(1),

    /**
     * 市外配送
     */
    OUTER_CITY_DELIVERY(2),

    /**
     * 即参与过"市内配送"也参与过“市外配送”
     */
    MIXTURE_CITY_DELIVERY(3);

    /**
     * 定义私有变量
     */
    private int deliveryAreaNum;

    private DeliveryArea(int deliveryAreaNum) {
        this.deliveryAreaNum = deliveryAreaNum;
    }


    @Override
    public String toString() {
        return String.valueOf(this.deliveryAreaNum);
    }

    public int index() {
        return deliveryAreaNum;
    }

    /**
     * 根据中文的提货方式，返回提货Id
     *
     * @param deliveryName
     * @return
     */
    public static int getDeliveryAreaNum(String deliveryName) {
        int num = 0;
        if (deliveryName.contains(Constant.INNER_CITY_DELIVERY)) {
            num = INNER_CITY_DELIVERY.deliveryAreaNum;
        }
        if (deliveryName.contains(Constant.OUTER_CITY_DELIVERY)) {
            num = OUTER_CITY_DELIVERY.deliveryAreaNum;
        }
        if (num == 0) {
            System.out.println("‘" + deliveryName + " ’配送方式不存在！ ！ ！请联系技术人员增加相应的配送方式");

        }
        return num;
    }

    /**
     * 获得对应的中文名称
     *
     * @param deliveryAreaNum
     * @return
     */
    public static String getDeliveryAreaName(int deliveryAreaNum) {
        if (deliveryAreaNum == 1) {
            return Constant.INNER_CITY_DELIVERY;
        } else if (deliveryAreaNum == 2) {
            return Constant.OUTER_CITY_DELIVERY;
        } else {
            return null;
        }
    }
} 