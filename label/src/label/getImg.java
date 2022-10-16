package label;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
public class getImg {
    public static void main(String[] args) {
    	try {
            //读取原始图片
            BufferedImage image = ImageIO.read(new FileInputStream("4-1.png"));
            System.out.println("Width: " + image.getWidth());
            System.out.println("Height: " + image.getHeight());
            //调整图片大小
            BufferedImage newImage = ImageUtils.resizeImage(image,1500,750); //jframe.setSize(1510, 850);
            //图像缓冲区图片保存为图片文件(文件不存在会自动创建文件保存，文件存在会覆盖原文件保存)
            ImageIO.write(newImage, "jpg", new File("4-1.png"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}