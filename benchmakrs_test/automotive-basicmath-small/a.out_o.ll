; ModuleID = 'a.out_o.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.int_sqrt = type { i32, i32 }

@.str = private unnamed_addr constant [39 x i8] c"********* CUBIC FUNCTIONS ***********\0A\00", align 1
@.str.1 = private unnamed_addr constant [11 x i8] c"Solutions:\00", align 1
@.str.2 = private unnamed_addr constant [4 x i8] c" %f\00", align 1
@.str.3 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@.str.4 = private unnamed_addr constant [41 x i8] c"********* INTEGER SQR ROOTS ***********\0A\00", align 1
@.str.5 = private unnamed_addr constant [17 x i8] c"sqrt(%3d) = %2d\0A\00", align 1
@.str.6 = private unnamed_addr constant [17 x i8] c"\0Asqrt(%lX) = %X\0A\00", align 1
@.str.7 = private unnamed_addr constant [40 x i8] c"********* ANGLE CONVERSION ***********\0A\00", align 1
@.str.8 = private unnamed_addr constant [31 x i8] c"%3.0f degrees = %.12f radians\0A\00", align 1
@.str.9 = private unnamed_addr constant [1 x i8] zeroinitializer, align 1
@.str.10 = private unnamed_addr constant [31 x i8] c"%.12f radians = %3.0f degrees\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca double, align 8
  %3 = alloca double, align 8
  %4 = alloca double, align 8
  %5 = alloca double, align 8
  %6 = alloca double, align 8
  %7 = alloca double, align 8
  %8 = alloca double, align 8
  %9 = alloca double, align 8
  %10 = alloca double, align 8
  %11 = alloca double, align 8
  %12 = alloca double, align 8
  %13 = alloca double, align 8
  %14 = alloca double, align 8
  %15 = alloca double, align 8
  %16 = alloca double, align 8
  %17 = alloca double, align 8
  %18 = alloca [3 x double], align 16
  %19 = alloca double, align 8
  %20 = alloca i32, align 4
  %21 = alloca i32, align 4
  %22 = alloca i64, align 8
  %23 = alloca %struct.int_sqrt, align 4
  %24 = alloca i64, align 8
  store i32 0, i32* %1, align 4
  store double 1.000000e+00, double* %2, align 8
  store double -1.050000e+01, double* %3, align 8
  store double 3.200000e+01, double* %4, align 8
  store double -3.000000e+01, double* %5, align 8
  store double 1.000000e+00, double* %6, align 8
  store double -4.500000e+00, double* %7, align 8
  store double 1.700000e+01, double* %8, align 8
  store double -3.000000e+01, double* %9, align 8
  store double 1.000000e+00, double* %10, align 8
  store double -3.500000e+00, double* %11, align 8
  store double 2.200000e+01, double* %12, align 8
  store double -3.100000e+01, double* %13, align 8
  store double 1.000000e+00, double* %14, align 8
  store double -1.370000e+01, double* %15, align 8
  store double 1.000000e+00, double* %16, align 8
  store double -3.500000e+01, double* %17, align 8
  store i64 1072497001, i64* %22, align 8
  store i64 0, i64* %24, align 8
  %25 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([39 x i8], [39 x i8]* @.str, i64 0, i64 0))
  %26 = getelementptr inbounds [3 x double], [3 x double]* %18, i64 0, i64 0
  call void @SolveCubic(double 1.000000e+00, double -1.050000e+01, double 3.200000e+01, double -3.000000e+01, i32* %20, double* %26)
  %27 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.1, i64 0, i64 0))
  store i32 0, i32* %21, align 4
  br label %28

28:                                               ; preds = %32, %0
  %29 = phi i32 [ %37, %32 ], [ 0, %0 ]
  %30 = load i32, i32* %20, align 4
  %31 = icmp slt i32 %29, %30
  br i1 %31, label %32, label %38

32:                                               ; preds = %28
  %33 = sext i32 %29 to i64
  %34 = getelementptr inbounds [3 x double], [3 x double]* %18, i64 0, i64 %33
  %35 = load double, double* %34, align 8
  %36 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), double %35)
  %37 = add nsw i32 %29, 1
  store i32 %37, i32* %21, align 4
  br label %28

38:                                               ; preds = %28
  %39 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i64 0, i64 0))
  call void @SolveCubic(double 1.000000e+00, double -4.500000e+00, double 1.700000e+01, double -3.000000e+01, i32* %20, double* %26)
  %40 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.1, i64 0, i64 0))
  store i32 0, i32* %21, align 4
  br label %41

41:                                               ; preds = %45, %38
  %42 = phi i32 [ %50, %45 ], [ 0, %38 ]
  %43 = load i32, i32* %20, align 4
  %44 = icmp slt i32 %42, %43
  br i1 %44, label %45, label %51

45:                                               ; preds = %41
  %46 = sext i32 %42 to i64
  %47 = getelementptr inbounds [3 x double], [3 x double]* %18, i64 0, i64 %46
  %48 = load double, double* %47, align 8
  %49 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), double %48)
  %50 = add nsw i32 %42, 1
  store i32 %50, i32* %21, align 4
  br label %41

51:                                               ; preds = %41
  %52 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i64 0, i64 0))
  call void @SolveCubic(double 1.000000e+00, double -3.500000e+00, double 2.200000e+01, double -3.100000e+01, i32* %20, double* %26)
  %53 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.1, i64 0, i64 0))
  store i32 0, i32* %21, align 4
  br label %54

54:                                               ; preds = %58, %51
  %55 = phi i32 [ %64, %58 ], [ 0, %51 ]
  %56 = load i32, i32* %20, align 4
  %57 = icmp slt i32 %55, %56
  br i1 %57, label %58, label %65

58:                                               ; preds = %54
  %59 = sext i32 %55 to i64
  %60 = getelementptr inbounds [3 x double], [3 x double]* %18, i64 0, i64 %59
  %61 = load double, double* %60, align 8
  %62 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), double %61)
  %63 = load i32, i32* %21, align 4
  %64 = add nsw i32 %63, 1
  store i32 %64, i32* %21, align 4
  br label %54

65:                                               ; preds = %54
  %66 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i64 0, i64 0))
  call void @SolveCubic(double 1.000000e+00, double -1.370000e+01, double 1.000000e+00, double -3.500000e+01, i32* %20, double* %26)
  %67 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.1, i64 0, i64 0))
  store i32 0, i32* %21, align 4
  br label %68

68:                                               ; preds = %72, %65
  %69 = phi i32 [ %78, %72 ], [ 0, %65 ]
  %70 = load i32, i32* %20, align 4
  %71 = icmp slt i32 %69, %70
  br i1 %71, label %72, label %79

72:                                               ; preds = %68
  %73 = sext i32 %69 to i64
  %74 = getelementptr inbounds [3 x double], [3 x double]* %18, i64 0, i64 %73
  %75 = load double, double* %74, align 8
  %76 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), double %75)
  %77 = load i32, i32* %21, align 4
  %78 = add nsw i32 %77, 1
  store i32 %78, i32* %21, align 4
  br label %68

79:                                               ; preds = %68
  %80 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i64 0, i64 0))
  store double 1.000000e+00, double* %2, align 8
  br label %81

81:                                               ; preds = %121, %79
  %82 = phi double [ %122, %121 ], [ 1.000000e+00, %79 ]
  %83 = fcmp olt double %82, 1.000000e+01
  br i1 %83, label %84, label %123

84:                                               ; preds = %81
  store double 1.000000e+01, double* %3, align 8
  br label %85

85:                                               ; preds = %119, %84
  %86 = phi double [ %93, %119 ], [ %82, %84 ]
  %87 = phi double [ %120, %119 ], [ 1.000000e+01, %84 ]
  %88 = fcmp ogt double %87, 0.000000e+00
  br i1 %88, label %89, label %121

89:                                               ; preds = %85
  store double 5.000000e+00, double* %4, align 8
  br label %90

90:                                               ; preds = %117, %89
  %91 = phi double [ %98, %117 ], [ %87, %89 ]
  %92 = phi double [ %118, %117 ], [ 5.000000e+00, %89 ]
  %93 = phi double [ %99, %117 ], [ %86, %89 ]
  %94 = fcmp olt double %92, 1.500000e+01
  br i1 %94, label %95, label %119

95:                                               ; preds = %90
  store double -1.000000e+00, double* %5, align 8
  br label %96

96:                                               ; preds = %114, %95
  %97 = phi double [ %116, %114 ], [ -1.000000e+00, %95 ]
  %98 = phi double [ %87, %114 ], [ %91, %95 ]
  %99 = phi double [ %82, %114 ], [ %93, %95 ]
  %100 = fcmp ogt double %97, -1.100000e+01
  br i1 %100, label %101, label %117

101:                                              ; preds = %96
  call void @SolveCubic(double %82, double %87, double %92, double %97, i32* %20, double* %26)
  %102 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.1, i64 0, i64 0))
  store i32 0, i32* %21, align 4
  br label %103

103:                                              ; preds = %107, %101
  %104 = phi i32 [ %113, %107 ], [ 0, %101 ]
  %105 = load i32, i32* %20, align 4
  %106 = icmp slt i32 %104, %105
  br i1 %106, label %107, label %114

107:                                              ; preds = %103
  %108 = sext i32 %104 to i64
  %109 = getelementptr inbounds [3 x double], [3 x double]* %18, i64 0, i64 %108
  %110 = load double, double* %109, align 8
  %111 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), double %110)
  %112 = load i32, i32* %21, align 4
  %113 = add nsw i32 %112, 1
  store i32 %113, i32* %21, align 4
  br label %103

114:                                              ; preds = %103
  %115 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i64 0, i64 0))
  %116 = fadd double %97, -1.000000e+00
  store double %116, double* %5, align 8
  br label %96

117:                                              ; preds = %96
  %118 = fadd double %92, 5.000000e-01
  store double %118, double* %4, align 8
  br label %90

119:                                              ; preds = %90
  %120 = fadd double %91, -1.000000e+00
  store double %120, double* %3, align 8
  br label %85

121:                                              ; preds = %85
  %122 = fadd double %86, 1.000000e+00
  store double %122, double* %2, align 8
  br label %81

123:                                              ; preds = %81
  %124 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.4, i64 0, i64 0))
  store i32 0, i32* %21, align 4
  br label %125

125:                                              ; preds = %128, %123
  %126 = phi i32 [ %135, %128 ], [ 0, %123 ]
  %127 = icmp slt i32 %126, 1001
  br i1 %127, label %128, label %136

128:                                              ; preds = %125
  %129 = sext i32 %126 to i64
  call void @usqrt(i64 %129, %struct.int_sqrt* %23)
  %130 = load i32, i32* %21, align 4
  %131 = getelementptr inbounds %struct.int_sqrt, %struct.int_sqrt* %23, i32 0, i32 0
  %132 = load i32, i32* %131, align 4
  %133 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([17 x i8], [17 x i8]* @.str.5, i64 0, i64 0), i32 %130, i32 %132)
  %134 = load i32, i32* %21, align 4
  %135 = add nsw i32 %134, 1
  store i32 %135, i32* %21, align 4
  br label %125

136:                                              ; preds = %125
  call void @usqrt(i64 1072497001, %struct.int_sqrt* %23)
  %137 = getelementptr inbounds %struct.int_sqrt, %struct.int_sqrt* %23, i32 0, i32 0
  %138 = load i32, i32* %137, align 4
  %139 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([17 x i8], [17 x i8]* @.str.6, i64 0, i64 0), i64 1072497001, i32 %138)
  %140 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([40 x i8], [40 x i8]* @.str.7, i64 0, i64 0))
  store double 0.000000e+00, double* %19, align 8
  br label %141

141:                                              ; preds = %144, %136
  %142 = phi double [ %149, %144 ], [ 0.000000e+00, %136 ]
  %143 = fcmp ole double %142, 3.600000e+02
  br i1 %143, label %144, label %150

144:                                              ; preds = %141
  %145 = call double @atan(double 1.000000e+00) #5
  %146 = fmul double %142, 0x400921FB54442D18
  %147 = fdiv double %146, 1.800000e+02
  %148 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.str.8, i64 0, i64 0), double %142, double %147)
  %149 = fadd double %142, 1.000000e+00
  store double %149, double* %19, align 8
  br label %141

150:                                              ; preds = %141
  %151 = call i32 @puts(i8* getelementptr inbounds ([1 x i8], [1 x i8]* @.str.9, i64 0, i64 0))
  store double 0.000000e+00, double* %19, align 8
  br label %152

152:                                              ; preds = %156, %150
  %153 = phi double [ %162, %156 ], [ 0.000000e+00, %150 ]
  %154 = call double @atan(double 1.000000e+00) #5
  %155 = fcmp ole double %153, 0x401921FB97600B9B
  br i1 %155, label %156, label %163

156:                                              ; preds = %152
  %157 = fmul double %153, 1.800000e+02
  %158 = call double @atan(double 1.000000e+00) #5
  %159 = fdiv double %157, 0x400921FB54442D18
  %160 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.str.10, i64 0, i64 0), double %153, double %159)
  %161 = call double @atan(double 1.000000e+00) #5
  %162 = fadd double %153, 0x3F91DF46A2529D39
  store double %162, double* %19, align 8
  br label %152

163:                                              ; preds = %152
  ret i32 0
}

declare dso_local i32 @printf(i8*, ...) #1

; Function Attrs: nounwind
declare dso_local double @atan(double) #2

declare dso_local i32 @puts(i8*) #1

; Function Attrs: noinline nounwind uwtable
define dso_local void @SolveCubic(double %0, double %1, double %2, double %3, i32* %4, double* %5) #0 {
  %7 = alloca double, align 8
  %8 = alloca double, align 8
  %9 = alloca double, align 8
  %10 = alloca double, align 8
  %11 = alloca i32*, align 8
  %12 = alloca double*, align 8
  %13 = alloca x86_fp80, align 16
  %14 = alloca x86_fp80, align 16
  %15 = alloca x86_fp80, align 16
  %16 = alloca x86_fp80, align 16
  %17 = alloca double, align 8
  %18 = alloca double, align 8
  %19 = alloca double, align 8
  store double %0, double* %7, align 8
  store double %1, double* %8, align 8
  store double %2, double* %9, align 8
  store double %3, double* %10, align 8
  store i32* %4, i32** %11, align 8
  store double* %5, double** %12, align 8
  %20 = fdiv double %1, %0
  %21 = fpext double %20 to x86_fp80
  store x86_fp80 %21, x86_fp80* %13, align 16
  %22 = fdiv double %2, %0
  %23 = fpext double %22 to x86_fp80
  store x86_fp80 %23, x86_fp80* %14, align 16
  %24 = fdiv double %3, %0
  %25 = fpext double %24 to x86_fp80
  store x86_fp80 %25, x86_fp80* %15, align 16
  %26 = fmul x86_fp80 %21, %21
  %27 = fmul x86_fp80 0xK4000C000000000000000, %23
  %28 = fsub x86_fp80 %26, %27
  %29 = fdiv x86_fp80 %28, 0xK40029000000000000000
  store x86_fp80 %29, x86_fp80* %16, align 16
  %30 = fmul x86_fp80 0xK40008000000000000000, %21
  %31 = fmul x86_fp80 %30, %21
  %32 = fmul x86_fp80 %31, %21
  %33 = fmul x86_fp80 0xK40029000000000000000, %21
  %34 = fmul x86_fp80 %33, %23
  %35 = fsub x86_fp80 %32, %34
  %36 = fmul x86_fp80 0xK4003D800000000000000, %25
  %37 = fadd x86_fp80 %35, %36
  %38 = fdiv x86_fp80 %37, 0xK4004D800000000000000
  %39 = fptrunc x86_fp80 %38 to double
  store double %39, double* %17, align 8
  %40 = fmul double %39, %39
  %41 = fpext double %40 to x86_fp80
  %42 = fmul x86_fp80 %29, %29
  %43 = fmul x86_fp80 %42, %29
  %44 = fsub x86_fp80 %41, %43
  %45 = fptrunc x86_fp80 %44 to double
  store double %45, double* %18, align 8
  %46 = fcmp ole double %45, 0.000000e+00
  br i1 %46, label %47, label %84

47:                                               ; preds = %6
  store i32 3, i32* %4, align 4
  %48 = fptrunc x86_fp80 %43 to double
  %49 = call double @sqrt(double %48) #5
  %50 = fdiv double %39, %49
  %51 = call double @acos(double %50) #5
  store double %51, double* %19, align 8
  %52 = fptrunc x86_fp80 %29 to double
  %53 = call double @sqrt(double %52) #5
  %54 = fmul double -2.000000e+00, %53
  %55 = fdiv double %51, 3.000000e+00
  %56 = call double @cos(double %55) #5
  %57 = fmul double %54, %56
  %58 = fpext double %57 to x86_fp80
  %59 = fdiv x86_fp80 %21, 0xK4000C000000000000000
  %60 = fsub x86_fp80 %58, %59
  %61 = fptrunc x86_fp80 %60 to double
  store double %61, double* %5, align 8
  %62 = call double @sqrt(double %52) #5
  %63 = fmul double -2.000000e+00, %62
  %64 = call double @atan(double 1.000000e+00) #5
  %65 = fadd double %51, 0x401921FB54442D18
  %66 = fdiv double %65, 3.000000e+00
  %67 = call double @cos(double %66) #5
  %68 = fmul double %63, %67
  %69 = fpext double %68 to x86_fp80
  %70 = fsub x86_fp80 %69, %59
  %71 = fptrunc x86_fp80 %70 to double
  %72 = getelementptr inbounds double, double* %5, i64 1
  store double %71, double* %72, align 8
  %73 = call double @sqrt(double %52) #5
  %74 = fmul double -2.000000e+00, %73
  %75 = call double @atan(double 1.000000e+00) #5
  %76 = fadd double %51, 0x402921FB54442D18
  %77 = fdiv double %76, 3.000000e+00
  %78 = call double @cos(double %77) #5
  %79 = fmul double %74, %78
  %80 = fpext double %79 to x86_fp80
  %81 = fsub x86_fp80 %80, %59
  %82 = fptrunc x86_fp80 %81 to double
  %83 = getelementptr inbounds double, double* %5, i64 2
  store double %82, double* %83, align 8
  br label %102

84:                                               ; preds = %6
  store i32 1, i32* %4, align 4
  %85 = call double @sqrt(double %45) #5
  %86 = call double @llvm.fabs.f64(double %39)
  %87 = fadd double %85, %86
  %88 = call double @pow(double %87, double 0x3FD5555555555555) #5
  %89 = fpext double %88 to x86_fp80
  %90 = fdiv x86_fp80 %29, %89
  %91 = fadd x86_fp80 %89, %90
  %92 = fptrunc x86_fp80 %91 to double
  %93 = fcmp olt double %39, 0.000000e+00
  %94 = zext i1 %93 to i64
  %95 = select i1 %93, i32 1, i32 -1
  %96 = sitofp i32 %95 to double
  %97 = fmul double %92, %96
  %98 = fdiv x86_fp80 %21, 0xK4000C000000000000000
  %99 = fpext double %97 to x86_fp80
  %100 = fsub x86_fp80 %99, %98
  %101 = fptrunc x86_fp80 %100 to double
  store double %101, double* %5, align 8
  br label %102

102:                                              ; preds = %84, %47
  ret void
}

; Function Attrs: nounwind
declare dso_local double @sqrt(double) #2

; Function Attrs: nounwind
declare dso_local double @acos(double) #2

; Function Attrs: nounwind
declare dso_local double @cos(double) #2

; Function Attrs: nounwind readnone speculatable willreturn
declare double @llvm.fabs.f64(double) #3

; Function Attrs: nounwind
declare dso_local double @pow(double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local void @usqrt(i64 %0, %struct.int_sqrt* %1) #0 {
  %3 = alloca i64, align 8
  %4 = alloca %struct.int_sqrt*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i64, align 8
  %8 = alloca i32, align 4
  store i64 %0, i64* %3, align 8
  store %struct.int_sqrt* %1, %struct.int_sqrt** %4, align 8
  store i64 0, i64* %5, align 8
  store i64 0, i64* %6, align 8
  store i64 0, i64* %7, align 8
  store i32 0, i32* %8, align 4
  br label %9

9:                                                ; preds = %28, %2
  %10 = phi i64 [ %29, %28 ], [ 0, %2 ]
  %11 = phi i64 [ %20, %28 ], [ %0, %2 ]
  %12 = phi i64 [ %30, %28 ], [ 0, %2 ]
  %13 = phi i32 [ %31, %28 ], [ 0, %2 ]
  %14 = icmp slt i32 %13, 32
  br i1 %14, label %15, label %32

15:                                               ; preds = %9
  %16 = shl i64 %12, 2
  %17 = and i64 %11, 3221225472
  %18 = lshr i64 %17, 30
  %19 = add i64 %16, %18
  store i64 %19, i64* %6, align 8
  %20 = shl i64 %11, 2
  store i64 %20, i64* %3, align 8
  %21 = shl i64 %10, 1
  store i64 %21, i64* %5, align 8
  %22 = shl i64 %21, 1
  %23 = add i64 %22, 1
  store i64 %23, i64* %7, align 8
  %24 = icmp uge i64 %19, %23
  br i1 %24, label %25, label %28

25:                                               ; preds = %15
  %26 = sub i64 %19, %23
  store i64 %26, i64* %6, align 8
  %27 = add i64 %21, 1
  store i64 %27, i64* %5, align 8
  br label %28

28:                                               ; preds = %25, %15
  %29 = phi i64 [ %27, %25 ], [ %21, %15 ]
  %30 = phi i64 [ %26, %25 ], [ %19, %15 ]
  %31 = add nsw i32 %13, 1
  store i32 %31, i32* %8, align 4
  br label %9

32:                                               ; preds = %9
  %33 = bitcast %struct.int_sqrt* %1 to i8*
  %34 = bitcast i64* %5 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 4 %33, i8* align 8 %34, i64 8, i1 false)
  ret void
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* noalias nocapture writeonly, i8* noalias nocapture readonly, i64, i1 immarg) #4

; Function Attrs: noinline nounwind uwtable
define dso_local double @rad2deg(double %0) #0 {
  %2 = fmul double 1.800000e+02, %0
  %3 = call double @atan(double 1.000000e+00) #5
  %4 = fdiv double %2, 0x400921FB54442D18
  ret double %4
}

; Function Attrs: noinline nounwind uwtable
define dso_local double @deg2rad(double %0) #0 {
  %2 = call double @atan(double 1.000000e+00) #5
  %3 = fmul double 0x400921FB54442D18, %0
  %4 = fdiv double %3, 1.800000e+02
  ret double %4
}

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readnone speculatable willreturn }
attributes #4 = { argmemonly nounwind willreturn }
attributes #5 = { nounwind }

!llvm.ident = !{!0, !0, !0, !0}
!llvm.module.flags = !{!1}

!0 = !{!"clang version 10.0.0-4ubuntu1 "}
!1 = !{i32 1, !"wchar_size", i32 4}
