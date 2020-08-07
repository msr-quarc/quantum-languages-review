# Q# Docker container

## Running this sample

To build and run this sample, execute the following commands:

```
cd src/qsharp
docker build -t qsharp .
docker run -it qsharp
dotnet test
```

## Building and running other Q# code

Q# leverages uses dotnet for execution. 
A new Q# console application can be created and run by executing the command
```cmd
dotnet new console -lang Q# -o /src/my_app && cd /src/my_app/
dotnet run
```

A new Q# test project can be created and run by executing the command
```cmd
dotnet new xunit -lang Q# -o /src/my_tests && cd /src/my_tests/
dotnet test
```
