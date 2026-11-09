package noob.ymuu.detour;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.fragment.app.Fragment;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
/* loaded from: classes.dex */
public class DiagnosticsFragment extends Fragment {
    @Override // androidx.fragment.app.Fragment
    public View onCreateView(LayoutInflater layoutInflater, ViewGroup viewGroup, Bundle bundle) {
        return layoutInflater.inflate(R.layout.fragment_diagnostics, viewGroup, false);
    }

    @Override // androidx.fragment.app.Fragment
    public void onViewCreated(View view, Bundle bundle) {
        super.onViewCreated(view, bundle);
        ((TextView) view.findViewById(R.id.tokenView)).setText(readToken());
    }

    private String readToken() {
        try {
            InputStream open = requireContext().getAssets().open("config.dat");
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            byte[] bArr = new byte[4096];
            while (true) {
                int read = open.read(bArr);
                if (read <= 0) {
                    break;
                }
                byteArrayOutputStream.write(bArr, 0, read);
            }
            String str = NativeBridge.token(byteArrayOutputStream.toByteArray());
            if (open != null) {
                open.close();
            }
            return str;
        } catch (Exception unused) {
            return "";
        }
    }
}
