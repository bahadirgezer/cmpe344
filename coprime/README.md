# RISC-V Coprime Program

This program determines if value pairs in the input array are coprime or not. Input values are hardcoded into the `coprime.s` file. The array should be of size `3n` where `n` is some positive integer. Each triple starts with two values which will be the input number pairs. The third value will be the output. If the two numbers are coprime the third value will be 1, if they are not coprime then it will be 2. 

## Assemble and Link

Use the Makefile to assemble, dissassemble and run the program. 

```
make
```

## Simulate using Whisper

Our desktop computers usually have processors with the `x86-64` architecture. Therefore, we cannot natively execute programs like `coprime.elf` on our computers. We use RISC-V ISA simulators like `whisper` to simulate a RISC-V processor on our desktop computers and execute RISC-V executables. The `whisper` simulator is a production-grade simulator installed in our lab environment. Please check the `whisper` application first using the command:

```
whisper --help
```
You should see the help text of the `whisper` simulator with various commands and flags. Then everything is fine.

We first use the simulator in the interactive mode, where we can instruct commands to the simulator. To start the simulation of `coprime.elf` in the interactive mode, please run the command in your terminal as follows:

```
whisper --interactive coprime.elf
```

Now you are in the interactive mode where you can give commands to the simulator. You can find the most commonly used commands for `whisper` in the following table.

| Interactive commands | Description                                                |
|----------------------|------------------------------------------------------------|
| `step [<N>]`         | Proceed `N` steps, default is 1.                           |
| `until <ADDR>`       | Proceed until reaching the address `ADDR`                  |
| `peek r <REG>`       | Print the current content of the register `REG`            |
| `peek m <ADDR>`      | Print the current content of the memory location at `ADDR` |
| `quit`               | Quit the simulation and interactive mode                   |

You can find other commands for `whisper` as listed in their docs [here](https://github.com/chipsalliance/SweRV-ISS).
