FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv openjdk-17-jdk unzip wget xz-utils file binutils && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN wget -q https://github.com/iBotPeaches/Apktool/releases/download/v2.9.3/apktool_2.9.3.jar -O /usr/local/bin/apktool.jar && chmod +x /usr/local/bin/apktool.jar
RUN wget -q https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip -O /tmp/jadx.zip && unzip -q /tmp/jadx.zip -d /opt/ && rm /tmp/jadx.zip && ln -s /opt/jadx-1.4.7/bin/jadx /usr/local/bin/jadx
RUN wget -q https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0.3_build/ghidra_11.0.3_PUBLIC_20240410.zip -O /tmp/ghidra.zip && unzip -q /tmp/ghidra.zip -d /opt/ && rm /tmp/ghidra.zip && ln -s /opt/ghidra_11.0.3_PUBLIC/support/analyzeHeadless /usr/local/bin/analyzeHeadless
COPY . .
ENTRYPOINT ["python3", "main.py"]
CMD ["--help"]
