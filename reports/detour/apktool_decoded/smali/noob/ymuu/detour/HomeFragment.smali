.class public Lnoob/ymuu/detour/HomeFragment;
.super Landroidx/fragment/app/Fragment;
.source "HomeFragment.java"


# direct methods
.method public static synthetic $r8$lambda$OTqjcyLxt4p6sEeh49yOuJc8A7M(Lnoob/ymuu/detour/HomeFragment;Landroid/view/View;)V
    .locals 0

    invoke-direct {p0, p1}, Lnoob/ymuu/detour/HomeFragment;->lambda$onViewCreated$0(Landroid/view/View;)V

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 12
    invoke-direct {p0}, Landroidx/fragment/app/Fragment;-><init>()V

    return-void
.end method

.method private synthetic lambda$onViewCreated$0(Landroid/view/View;)V
    .locals 1

    .line 22
    invoke-static {p0}, Landroidx/navigation/fragment/NavHostFragment;->findNavController(Landroidx/fragment/app/Fragment;)Landroidx/navigation/NavController;

    move-result-object p1

    sget v0, Lnoob/ymuu/detour/R$id;->toSupport:I

    invoke-virtual {p1, v0}, Landroidx/navigation/NavController;->navigate(I)V

    return-void
.end method


# virtual methods
.method public onCreateView(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;
    .locals 1

    .line 16
    sget p3, Lnoob/ymuu/detour/R$layout;->fragment_home:I

    const/4 v0, 0x0

    invoke-virtual {p1, p3, p2, v0}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;Z)Landroid/view/View;

    move-result-object p1

    return-object p1
.end method

.method public onViewCreated(Landroid/view/View;Landroid/os/Bundle;)V
    .locals 0

    .line 20
    invoke-super {p0, p1, p2}, Landroidx/fragment/app/Fragment;->onViewCreated(Landroid/view/View;Landroid/os/Bundle;)V

    .line 21
    sget p2, Lnoob/ymuu/detour/R$id;->openSupport:I

    invoke-virtual {p1, p2}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    move-result-object p1

    new-instance p2, Lnoob/ymuu/detour/HomeFragment$$ExternalSyntheticLambda0;

    invoke-direct {p2, p0}, Lnoob/ymuu/detour/HomeFragment$$ExternalSyntheticLambda0;-><init>(Lnoob/ymuu/detour/HomeFragment;)V

    invoke-virtual {p1, p2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    return-void
.end method
