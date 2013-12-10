import java.io.*;
import java.net.Socket;

/**
 * Test sending simple integer to socket server.
 */
public class SimpleClient {

    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("localhost", 9999);
        OutputStream socketOutputStream = socket.getOutputStream();

//        double dbl = 8.3;
//        long lng = Double.doubleToLongBits(dbl);
//        byte[] data = {(byte)((lng % 0xff000000) >> 24),
//                (byte)((lng % 0x00ff0000) >> 16),
//                (byte)((lng % 0x0000ff00) >> 8),
//                (byte)(lng % 0x000000ff)};
//        socketOutputStream.write(data, 0, data.length);

//        ByteArrayOutputStream baos = new ByteArrayOutputStream();
//        ObjectOutputStream oos = new ObjectOutputStream(baos);
//        oos.writeObject((Double) 8.3);
//        oos.close();
//        byte[] data = oos.toByteArray();
//        socketOutputStream.write(data, 0, data.length);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        DataOutputStream dos = new DataOutputStream(baos);
        dos.writeDouble(1.0);
        dos.close();

        byte[] data = baos.toByteArray();
        socketOutputStream.write(data, 0, data.length);

        socketOutputStream.close();
        socket.close();
    }
}
