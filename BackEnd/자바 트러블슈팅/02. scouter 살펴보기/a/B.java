package a;

import a.Z;

public class B {
    public static void main(String args[]) {
        B b = new B();
        b.c();
    }

    public void c() {
        try {
            while (true) {
                Thread.sleep(1000);
                d();
            }
        } catch (Exception e) {
        }
    }

    public void d() {
        try {
            Thread.sleep(1000);
            Z z = new Z();
            z.calculate(System.currentTimeMillis());
        } catch (Exception e) {
        }
    }
}