package Util;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * sql类数据库工具接口
 */
public class SqlDBUtil {

    /**
     * 链接sql数据库的接口
     * @param driver
     * @param url
     * @param user
     * @param password
     * @return
     */
    public static Connection getConnection(String driver, String url, String user, String password){
        Connection connection = null ;
        try {
            Class.forName(driver).newInstance();
            connection = DriverManager.getConnection(url,user,password);
        }catch (SQLException e){
            throw new SQLException("数据库链接失败 == ",e);
        }finally {
            return connection;
        }
    }

    /**
     * 关闭数据库
     * @param connection
     * @throws SQLException
     */
    public static void close(Connection connection)  {
        if (connection!=null){
            try {
                connection.close();
            }catch (SQLException e){
               e.printStackTrace();
            }finally {
                System.out.println("数据库关闭成功！！！");
            }
        }
    }
} 