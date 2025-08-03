public class Test {
    public static void main(String[] args) {
        // Test case 1: Simple ascending frequencies
        System.out.println("----- Test Case 1 -----");
        int[] testCase1 = {0, 1, 2, 3};
        printFrequencies(testCase1);
        System.out.println();

        // Test case 2: Larger range with zeros in between
        System.out.println("----- Test Case 2 -----");
        int[] testCase2 = {4, 3, 2, 1, 0, 1, 2, 3, 4};
        printFrequencies(testCase2);
        System.out.println();

        // Test case 3: All zeros
        System.out.println("----- Test Case 3 -----");
        int[] testCase3 = {0, 0, 0, 0, 0};
        printFrequencies(testCase3);
        System.out.println();

        // Test case 4: Single element
        System.out.println("----- Test Case 4 -----");
        int[] testCase4 = {10};
        printFrequencies(testCase4);
        System.out.println();

        // Test case 5: Arbitrary set of frequencies
        System.out.println("----- Test Case 5 -----");
        int[] testCase5 = {2, 0, 5, 1, 0, 3, 10};
        printFrequencies(testCase5);
        System.out.println();
    }

    public static void printFrequencies(int[] input) {
        for (int i = 0; i < input.length; i++) {
            // Printing according to the specified format:
            String asterisks = new String(new char[input[i]]).replace("\0", "*");
            System.out.printf("%02d: %2d = <%s>%n", i, input[i], asterisks);
        }
    }
}
