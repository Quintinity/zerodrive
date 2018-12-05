/*****************************************
* Zerodrive - a cloud storage webapp     *
* INFO 3103 Term Project                 *
* by Vlad Marica (3440500)               *
* Fall 2018                              *
*****************************************/

// Async function that sleeps for a given number of milliseconds
export async function sleep(ms: number): Promise<void> {
    return new Promise<void>((resolve, _) => {
        setTimeout(() => {
            resolve();
        }, ms);
    });
}
