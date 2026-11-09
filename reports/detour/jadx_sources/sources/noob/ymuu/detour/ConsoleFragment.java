package noob.ymuu.detour;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.fragment.app.Fragment;
/* loaded from: classes.dex */
public class ConsoleFragment extends Fragment {
    @Override // androidx.fragment.app.Fragment
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        Bundle arguments = getArguments();
        NativeBridge.feed(2, arguments != null ? arguments.getString("seg", "") : "");
    }

    @Override // androidx.fragment.app.Fragment
    public View onCreateView(LayoutInflater layoutInflater, ViewGroup viewGroup, Bundle bundle) {
        return layoutInflater.inflate(R.layout.fragment_console, viewGroup, false);
    }

    @Override // androidx.fragment.app.Fragment
    public void onViewCreated(View view, Bundle bundle) {
        super.onViewCreated(view, bundle);
        final TextView textView = (TextView) view.findViewById(R.id.output);
        view.findViewById(R.id.retrieve).setOnClickListener(new View.OnClickListener() { // from class: noob.ymuu.detour.ConsoleFragment$$ExternalSyntheticLambda0
            @Override // android.view.View.OnClickListener
            public final void onClick(View view2) {
                textView.setText(NativeBridge.unlock(NativeBridge.mangle(NativeBridge.drain())));
            }
        });
    }
}
