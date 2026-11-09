.class public Lnoob/ymuu/detour/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 7
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 0

    .line 9
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 10
    sget p1, Lnoob/ymuu/detour/R$layout;->activity_main:I

    invoke-virtual {p0, p1}, Lnoob/ymuu/detour/MainActivity;->setContentView(I)V

    return-void
.end method

.method protected onNewIntent(Landroid/content/Intent;)V
    .locals 0

    .line 14
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onNewIntent(Landroid/content/Intent;)V

    .line 15
    invoke-virtual {p0, p1}, Lnoob/ymuu/detour/MainActivity;->setIntent(Landroid/content/Intent;)V

    return-void
.end method
