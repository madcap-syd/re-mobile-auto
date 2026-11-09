.class public final Lnoob/ymuu/detour/NativeBridge;
.super Ljava/lang/Object;
.source "NativeBridge.java"


# static fields
.field private static final M1_CONSTS:[I


# direct methods
.method static constructor <clinit>()V
    .locals 4

    .line 5
    const-string v0, "detour"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    const v0, -0x3d4d51cb

    const v1, 0x27d4eb2f

    const v2, -0x61c8864f

    const v3, -0x7a143595

    .line 21
    filled-new-array {v2, v3, v0, v1}, [I

    move-result-object v0

    sput-object v0, Lnoob/ymuu/detour/NativeBridge;->M1_CONSTS:[I

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 7
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static native drain()[B
.end method

.method public static native feed(ILjava/lang/String;)V
.end method

.method public static mangle([B)[B
    .locals 9

    if-eqz p0, :cond_5

    .line 31
    array-length v0, p0

    const/16 v1, 0x30

    if-eq v0, v1, :cond_0

    goto/16 :goto_4

    :cond_0
    const/16 v0, 0xc

    .line 32
    new-array v2, v0, [I

    const/4 v3, 0x0

    move v4, v3

    :goto_0
    const/16 v5, 0x8

    if-ge v4, v0, :cond_1

    mul-int/lit8 v6, v4, 0x4

    .line 34
    aget-byte v7, p0, v6

    and-int/lit16 v7, v7, 0xff

    shl-int/lit8 v7, v7, 0x18

    add-int/lit8 v8, v6, 0x1

    aget-byte v8, p0, v8

    and-int/lit16 v8, v8, 0xff

    shl-int/lit8 v8, v8, 0x10

    or-int/2addr v7, v8

    add-int/lit8 v8, v6, 0x2

    aget-byte v8, p0, v8

    and-int/lit16 v8, v8, 0xff

    shl-int/lit8 v5, v8, 0x8

    or-int/2addr v5, v7

    add-int/lit8 v6, v6, 0x3

    aget-byte v6, p0, v6

    and-int/lit16 v6, v6, 0xff

    or-int/2addr v5, v6

    aput v5, v2, v4

    add-int/lit8 v4, v4, 0x1

    goto :goto_0

    :cond_1
    move p0, v3

    :goto_1
    if-ge p0, v5, :cond_3

    move v4, v3

    :goto_2
    if-ge v4, v0, :cond_2

    .line 39
    aget v6, v2, v4

    sget-object v7, Lnoob/ymuu/detour/NativeBridge;->M1_CONSTS:[I

    add-int v8, v4, p0

    and-int/lit8 v8, v8, 0x3

    aget v7, v7, v8

    add-int/2addr v6, v7

    aput v6, v2, v4

    add-int/lit8 v7, v4, 0x5

    .line 40
    rem-int/2addr v7, v0

    aget v7, v2, v7

    mul-int/lit8 v8, p0, 0x3

    add-int/2addr v8, v4

    and-int/lit8 v8, v8, 0x1f

    invoke-static {v7, v8}, Ljava/lang/Integer;->rotateLeft(II)I

    move-result v7

    xor-int/2addr v6, v7

    aput v6, v2, v4

    const/4 v7, 0x7

    .line 41
    invoke-static {v6, v7}, Ljava/lang/Integer;->rotateLeft(II)I

    move-result v6

    aput v6, v2, v4

    add-int/lit8 v4, v4, 0x1

    goto :goto_2

    :cond_2
    add-int/lit8 p0, p0, 0x1

    goto :goto_1

    .line 44
    :cond_3
    new-array p0, v1, [B

    :goto_3
    if-ge v3, v0, :cond_4

    mul-int/lit8 v1, v3, 0x4

    .line 46
    aget v4, v2, v3

    ushr-int/lit8 v5, v4, 0x18

    int-to-byte v5, v5

    aput-byte v5, p0, v1

    add-int/lit8 v5, v1, 0x1

    ushr-int/lit8 v6, v4, 0x10

    int-to-byte v6, v6

    .line 47
    aput-byte v6, p0, v5

    add-int/lit8 v5, v1, 0x2

    ushr-int/lit8 v6, v4, 0x8

    int-to-byte v6, v6

    .line 48
    aput-byte v6, p0, v5

    add-int/lit8 v1, v1, 0x3

    int-to-byte v4, v4

    .line 49
    aput-byte v4, p0, v1

    add-int/lit8 v3, v3, 0x1

    goto :goto_3

    :cond_4
    return-object p0

    :cond_5
    :goto_4
    const/4 p0, 0x0

    return-object p0
.end method

.method public static native token([B)Ljava/lang/String;
.end method

.method public static native unlock([B)Ljava/lang/String;
.end method
