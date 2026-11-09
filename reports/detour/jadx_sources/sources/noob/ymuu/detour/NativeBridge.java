package noob.ymuu.detour;

import kotlin.UByte;
/* loaded from: classes.dex */
public final class NativeBridge {
    private static final int[] M1_CONSTS;

    public static native byte[] drain();

    public static native void feed(int i, String str);

    public static native String token(byte[] bArr);

    public static native String unlock(byte[] bArr);

    static {
        System.loadLibrary("detour");
        M1_CONSTS = new int[]{-1640531535, -2048144789, -1028477387, 668265263};
    }

    private NativeBridge() {
    }

    public static byte[] mangle(byte[] bArr) {
        if (bArr == null || bArr.length != 48) {
            return null;
        }
        int[] iArr = new int[12];
        for (int i = 0; i < 12; i++) {
            int i2 = i * 4;
            iArr[i] = ((bArr[i2 + 2] & UByte.MAX_VALUE) << 8) | ((bArr[i2] & UByte.MAX_VALUE) << 24) | ((bArr[i2 + 1] & UByte.MAX_VALUE) << 16) | (bArr[i2 + 3] & UByte.MAX_VALUE);
        }
        for (int i3 = 0; i3 < 8; i3++) {
            for (int i4 = 0; i4 < 12; i4++) {
                int i5 = iArr[i4] + M1_CONSTS[(i4 + i3) & 3];
                iArr[i4] = i5;
                int rotateLeft = i5 ^ Integer.rotateLeft(iArr[(i4 + 5) % 12], ((i3 * 3) + i4) & 31);
                iArr[i4] = rotateLeft;
                iArr[i4] = Integer.rotateLeft(rotateLeft, 7);
            }
        }
        byte[] bArr2 = new byte[48];
        for (int i6 = 0; i6 < 12; i6++) {
            int i7 = i6 * 4;
            int i8 = iArr[i6];
            bArr2[i7] = (byte) (i8 >>> 24);
            bArr2[i7 + 1] = (byte) (i8 >>> 16);
            bArr2[i7 + 2] = (byte) (i8 >>> 8);
            bArr2[i7 + 3] = (byte) i8;
        }
        return bArr2;
    }
}
