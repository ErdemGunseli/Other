
class Algorithms{

    public static void main(String[] args) {
        // The main method is called when the program is run:
        Algorithms algorithms = new Algorithms();

        int[] values = new int[]{1, 4, 3, 5, 6, 3, 4, 6, 4};
        values = algorithms.bubbleSort(values);

        for (int value: values) {
            System.out.println(value);
        }
    }

    public int linearSearch(String[] values, String target){
        int index = 0;

        while (index < values.length) {
            if (values[index].equals(target)){
                return index;
            }
            index++;
        }
        return -1;
}

    public int recursiveBinarySearch(int[] values, int target, int start, int end){
        int midpoint = (start + end) / 2;

        if (start > end){return -1;}
        else if (target < values[midpoint]){return recursiveBinarySearch(values, target, start, midpoint-1);}
        else if (values[midpoint] < target){return recursiveBinarySearch(values, target, midpoint+1, end);}
        
        return midpoint;
    }

    public int iterativeBinarySearch(int[] values, int target){
        int midpoint;
        int start = 0;
        int end = values.length - 1;

        while (start <= end){
            midpoint = (start + end) / 2;
            
            if (target < values[midpoint]){end = midpoint - 1;}
            else if (values[midpoint] < target){start = midpoint + 1;}
            else {return midpoint;}
        }
        return -1;
    }

    public int[] bubbleSort(int[] values){
        int temp;
        boolean sorted = false;

        while (!sorted) {
            sorted = true;

            for (int index=0; index<values.length-1; index++){
                if (values[index] > values[index+1]){
                    sorted = false;

                    temp = values[index];
                    values[index] = values[index+1];
                    values[index+1] = temp;
                }
            }
        }
        return values;
    }

    public int[] insertionSort(int[] values){
        int index = 1;
        int position;
        int currentValue;

        while (index < values.length){
            currentValue = values[index];
            position = index;

            while (position > 0 && currentValue < values[position - 1]){
                values[position] = values[position - 1];
                position --;
            }
            values[position] = currentValue;
            index ++;
        }

        return values;
    }

    }
