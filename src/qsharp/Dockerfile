FROM mcr.microsoft.com/quantum/iqsharp-base:0.12.2007.124

USER root

# Copy Q# projects over from the build context.
COPY Teleport.csproj /src/sample/
COPY *.qs /src/sample/

RUN chown -R ${USER}:${USER} /src
USER ${USER}

WORKDIR /src/sample
RUN dotnet restore

ENTRYPOINT [ "/bin/bash" ]

