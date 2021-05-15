package com.company;

import java.util.Random;
import java.util.concurrent.Semaphore;

public class Vectors {

    private static final int TESTS_NR = 50;

    private static Random r = new Random();

    private static class ScalarProduct implements Runnable {

        private Vector v1;

        private Vector v2;

        private int start;

        private int end;

        private static Semaphore mutex = new Semaphore(1, true);

        private static int scalar_product = 0;

        public ScalarProduct(Vector v1, Vector v2, int start, int end) {
            this.v1 = v1;
            this.v2 = v2;
            this.start = start;
            this.end = end;
        }

        @Override
        public void run() {
            for (int i = start; i <= end; i++) {
                int x = v1.coordinates[i] * v2.coordinates[i];
                try {
                    mutex.acquire();
                } catch (InterruptedException e) {
                    System.out.println(e);
                    Thread.currentThread().interrupt();
                }
                scalar_product += x;
                mutex.release();
            }
        }
    }

    private static class Sum implements Runnable {

        private Vector v1;

        private Vector v2;

        private Vector sum_of_vectors;

        private int start;

        private int end;

        public Sum(Vector v1, Vector v2, Vector sum_of_vectors, int start, int end) {
            this.v1 = v1;
            this.v2 = v2;
            this.sum_of_vectors = sum_of_vectors;
            this.start = start;
            this.end = end;
        }

        @Override
        public void run() {
            for (int i = start; i <= end; i++) {
                int x = v1.coordinates[i] + v2.coordinates[i];
                sum_of_vectors.coordinates[i] = x;
            }
        }
    }


    private static class Vector {

        private int size;

        private int[] coordinates;

        public Vector(int[] coordinates) {
            this.coordinates = coordinates;
            this.size = coordinates.length;
        }

        public Vector sum(Vector v) {
            if (v.size != this.size)
                throw new IllegalArgumentException("Wektory muszą mieć równą długość.");

            int[] coordinates = new int[this.coordinates.length];
            Vector sum_of_vectors = new Vector(coordinates);

            int threads_nr = size / 10;
            if (size % 10 != 0)
                threads_nr++;

            Thread[] threads_array = new Thread[threads_nr];

            for (int i = 0; i < threads_nr; i++) {
                int start = 10 * i;
                int end = 10 * i + 9;

                if (i == threads_nr - 1) { // ostatni wątek liczy najkrótszy blok
                    if (size % 10 != 0)
                        end = 10 * i + size % 10 - 1;
                }

                Runnable r = new Sum(this, v, sum_of_vectors, start, end);
                Thread t = new Thread(r, "Liczy sumę współrzędnych od " + start + " do " + end);
                threads_array[i] = t;
                t.start();
            }

            for (Thread t : threads_array) {
                try {
                    t.join();
                } catch (InterruptedException e) {
                    t.interrupt();
                }
            }
            return sum_of_vectors;
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < size; i++) {
                sb.append(coordinates[i]);
                if (i < size - 1)
                    sb.append(" ");
            }
            return sb.toString();
        }

        public int scalar_product(Vector v) {
            if (v.size != this.size)
                throw new IllegalArgumentException();

            int threads_nr = size / 10;
            if (size % 10 != 0)
                threads_nr++;

            Thread[] threads_array = new Thread[threads_nr];
            ScalarProduct.scalar_product = 0;

            for (int i = 0; i < threads_nr; i++) {
                int start = 10 * i;
                int end = 10 * i + 9;

                if (i == threads_nr - 1) { // ostatni wątek liczy najkrótszy blok
                    if (size % 10 != 0)
                        end = 10 * i + size % 10 - 1;
                }

                Runnable r = new ScalarProduct(this, v, start, end);
                Thread t = new Thread(r, "Liczy iloczyn skalarny współrzędnych od " + start + " do " + end);
                threads_array[i] = t;
                t.start();
            }

            for (Thread t : threads_array) {
                try {
                    t.join();
                } catch (InterruptedException e) {
                    t.interrupt();
                }
            }

            return ScalarProduct.scalar_product;
        }
    }

    private static void generateRandomArray(int[] A) {

        for (int i = 0; i < A.length; i++)
            A[i] = r.nextInt(10) + 1;

    }

    public static void main(String[] args) {

        int correct_sum = 0;

        int correct_scalar_product = 0;

        for (int k = 0; k < TESTS_NR; k++) {
            int n = r.nextInt(100) + 1;
            int[] A = new int[n];
            int[] B = new int[n];
            generateRandomArray(A);
            generateRandomArray(B);

            Vector v1 = new Vector(A);
            Vector v2 = new Vector(B);
            Vector sum_of_vectors = v1.sum(v2);

            boolean sum_of_vector_correct = true;
            for (int i = 0; i < n && sum_of_vector_correct; i++) {
                if (v1.coordinates[i] + v2.coordinates[i] != sum_of_vectors.coordinates[i]) {
                    sum_of_vector_correct = false;
                }
            }
            if (sum_of_vector_correct)
                correct_sum++;

            int scalar_product = 0;
            for (int i = 0; i < n; i++) {
                scalar_product += v1.coordinates[i] * v2.coordinates[i];
            }

            int scalar_product_with_threads = v1.scalar_product(v2);

            if (scalar_product == scalar_product_with_threads)
                correct_scalar_product++;

        }

        System.out.println(correct_sum + " z " + TESTS_NR + " testów na sumę wektorów przeszło poprawnie.");
        System.out.println(correct_scalar_product + " z " + TESTS_NR + " testów na iloczyn skalarny wektorów przeszło poprawnie.");

    }
}