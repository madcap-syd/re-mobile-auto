.class public Lnoob/ymuu/detour/ConsoleFragment;
.super Landroidx/fragment/app/Fragment;
.source "ConsoleFragment.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 12
    invoke-direct {p0}, Landroidx/fragment/app/Fragment;-><init>()V

    return-void
.end method

.method static synthetic lambda$onViewCreated$0(Landroid/widget/TextView;Landroid/view/View;)V
    .locals 0

    .line 30
    invoke-static {}, Lnoob/ymuu/detour/NativeBridge;->drain()[B

    move-result-object p1

    invoke-static {p1}, Lnoob/ymuu/detour/NativeBridge;->mangle([B)[B

    move-result-object p1

    .line 29
    invoke-static {p1}, Lnoob/ymuu/detour/NativeBridge;->unlock([B)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p0, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    return-void
.end method


# virtual methods
.method public onCreate(Landroid/os/Bundle;)V
    .locals 2

    .line 14
    invoke-super {p0, p1}, Landroidx/fragment/app/Fragment;->onCreate(Landroid/os/Bundle;)V

    .line 15
    invoke-virtual {p0}, Lnoob/ymuu/detour/ConsoleFragment;->getArguments()Landroid/os/Bundle;

    move-result-object p1

    .line 16
    const-string v0, ""

    if-nez p1, :cond_0

    goto :goto_0

    :cond_0
    const-string v1, "seg"

    invoke-virtual {p1, v1, v0}, Landroid/os/Bundle;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    :goto_0
    const/4 p1, 0x2

    invoke-static {p1, v0}, Lnoob/ymuu/detour/NativeBridge;->feed(ILjava/lang/String;)V

    return-void
.end method

.method public onCreateView(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;
    .locals 1

    .line 22
    sget p3, Lnoob/ymuu/detour/R$layout;->fragment_console:I

    const/4 v0, 0x0

    invoke-virtual {p1, p3, p2, v0}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;Z)Landroid/view/View;

    move-result-object p1

    return-object p1
.end method

.method public onViewCreated(Landroid/view/View;Landroid/os/Bundle;)V
    .locals 1

    .line 26
    invoke-super {p0, p1, p2}, Landroidx/fragment/app/Fragment;->onViewCreated(Landroid/view/View;Landroid/os/Bundle;)V

    .line 27
    sget p2, Lnoob/ymuu/detour/R$id;->output:I

    invoke-virtual {p1, p2}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    move-result-object p2

    check-cast p2, Landroid/widget/TextView;

    .line 28
    sget v0, Lnoob/ymuu/detour/R$id;->retrieve:I

    invoke-virtual {p1, v0}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    move-result-object p1

    new-instance v0, Lnoob/ymuu/detour/ConsoleFragment$$ExternalSyntheticLambda0;

    invoke-direct {v0, p2}, Lnoob/ymuu/detour/ConsoleFragment$$ExternalSyntheticLambda0;-><init>(Landroid/widget/TextView;)V

    invoke-virtual {p1, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    return-void
.end method
