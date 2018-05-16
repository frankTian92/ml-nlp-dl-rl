import dynamicPlanning.domain.DeliveryArea;
import org.junit.Test;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/9 0009
 * \* Time: 下午 15:21
 * \* Description: 测试提货方式
 * \
 */
import static org.junit.Assert.assertEquals;
public class DeliveryAreaTest {
    @Test
    public void testInnerCityDelivery(){
        String deliveryName = "市内配送";
        assertEquals("‘市内配送’测试结果 ： ",DeliveryArea.getDeliveryAreaNum(deliveryName),1);
        System.out.println("'市内配送'测试通过! ! !" );

    }

    @Test
    public void testOuterCityDelivery(){
        String deliveryName = "市外配送";
        assertEquals("‘市外配送’测试结果 ： ",DeliveryArea.getDeliveryAreaNum(deliveryName),2);
        System.out.println("'市外配送'测试通过! ! !" );

    }

    @Test
    public void testOtherCityDelivery(){
        String deliveryName = "其他配送";
        assertEquals("‘其他配送’测试结果 ： ",DeliveryArea.getDeliveryAreaNum(deliveryName),0);
        System.out.println("'其他配送'测试通过! ! !" );

    }

    @Test
    public void testDeliveryOrignal(){
        int innterIndex = 1;
        assertEquals("‘市内配送编号’测试结果 ：",DeliveryArea.INNER_CITY_DELIVERY.index(),1);
        System.out.println("'市内配送编号'测试通过! ! !" );
    }
}