; ModuleID = "synapse_module"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

@"fmt" = constant [4 x i8] c"%d\0a\00"
define i32 @"main"()
{
entry:
  %"x" = alloca i64
  store i64 10, i64* %"x"
  %"y" = alloca i64
  %"x_val" = load i64, i64* %"x"
  %"soma" = add i64 %"x_val", 100
  store i64 %"soma", i64* %"y"
  %"x_val.1" = load i64, i64* %"x"
  %".4" = bitcast [4 x i8]* @"fmt" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i64 %"x_val.1")
  %"y_val" = load i64, i64* %"y"
  %".6" = bitcast [4 x i8]* @"fmt" to i8*
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", i64 %"y_val")
  %".8" = bitcast [4 x i8]* @"fmt" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i64 50)
  %"z" = alloca i64
  %"y_val.1" = load i64, i64* %"y"
  %"soma.1" = add i64 %"y_val.1", 200
  store i64 %"soma.1", i64* %"z"
  %"z_val" = load i64, i64* %"z"
  %".11" = bitcast [4 x i8]* @"fmt" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", i64 %"z_val")
  ret i32 0
}
