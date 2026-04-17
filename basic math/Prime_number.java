import java.util.Scanner;

class Prime_number {
    public static void main(String args[]){

        Scanner sc = new Scanner(System.in);

        if(n <= 1){
           System.out.println(n + "number is not prime");
           return;
        }

        boolean prime = true;
        for(int i = 2; i*i<=n; i++){
            if(n % i == 0){
                prime = false;
                break;
             }
          }

          if(prime){
             System.out.println(n + "number is prime");
          }

          else{
             System.out.println(n + "number is not prime");
          }

        }
    }