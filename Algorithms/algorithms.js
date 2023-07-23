function linearSearch(values, target) {
    let index = 0;

    while (index < values.length) {
        if (values[index] == target) {return index;}
        index++;
    }
    return -1;
}

function recursiveBinarySearch(values, target, start=0, end=values.length -1) {
    let midpoint = Math.floor((start + end) / 2);

    if (start > end) {return -1;}
    else if (target < values[midpoint]) {return recursiveBinarySearch(values, target, start, midpoint - 1);}
    else if (values[midpoint] < target) {return recursiveBinarySearch(values, target, midpoint + 1, end);}


    return midpoint;
}

function iterativeBinarySearch(values, target) {
    let midpoint;
    let start = 0;
    let end = values.length - 1;

    while (start <= end) {
        midpoint = Math.floor((start + end) / 2);

        if (target < values[midpoint]) {end = midpoint - 1;}
        else if (values[midpoint] < target) {start = midpoint + 1;}
        else {return midpoint;}
    }
    return -1;
}

function bubbleSort(values) {
    let temp;
    let found = false;

    while (!found) {
        found = true;

        for (let index = 0; index < values.length - 1; index++) {
            if (values[index] > values[index+1]) {
                found = false;

                temp = values[index];
                values[index] = values[index+1];
                values[index+1] = temp;
            }
        }
    }

    return values;
}

function insertionSort(values) {
    let position;
    let currentValue;
    let index = 1;

    while (index < values.length) {
        currentValue = values[index];
        position = index;

        while (position > 0 && currentValue < values[position - 1]) {
            values[position] = values[position - 1];
            position--;
        }

        values[position] = currentValue;
        index ++;
    }
    return values;
}

let values = [5, 3, 7, 6, 2, 9, 1, 4, 8, 10, -1, 0];
console.log(insertionSort(values));
