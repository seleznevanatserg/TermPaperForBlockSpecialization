package task02;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FilterReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class janket {
    public static void main(String[] args) {
        String file = "task02/input.txt";
        List allProductsForJanket = new ArrayList<String>();


        try (FileReader fr = new FileReader(file)) {
            BufferedReader br = new BufferedReader(fr);
            String line = "";
            while((line = br.readLine()) != null) {
                
                String [] allProd = line.split(" ");
                for (String product : allProd){
                    allProductsForJanket.add(product);
                }
            }
            
            br.close();
        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        catch (IOException e) {
            System.out.println(e.toString());
        }

        // Количество слов в файле
        int counterWordsInFile = allProductsForJanket.size();
        System.out.println("Words in file: " + counterWordsInFile);
        
        // Самое длинное слово в файле
        String maxLongWordInFile = (String)allProductsForJanket.get(0);
        int maxLong = maxLongWordInFile.length();
        for (int i = 1; i < allProductsForJanket.size(); i++){
            int newMaxLong =((String)allProductsForJanket.get(i)).length();
            if (maxLong < newMaxLong){
                maxLong = newMaxLong;
                maxLongWordInFile = (String)allProductsForJanket.get(i);
            }
        }
        System.out.println("Long word: " + maxLongWordInFile + "  [length = " + maxLong + "]");

        // Частота употребления слов файле + сортировка по убыванию
        Map<String, Integer> counterProducts = new HashMap<String, Integer> ();
        for (int i = 0; i < allProductsForJanket.size(); i++){
            if (counterProducts.containsKey(allProductsForJanket.get(i))){
                counterProducts.put((String) allProductsForJanket.get(i),counterProducts.get(allProductsForJanket.get(i)) + 1); 
            }
            else{
                counterProducts.put((String) allProductsForJanket.get(i), 1); 
            }
        }
        Map<String, Integer> counterProductsSorted = new LinkedHashMap<String, Integer> ();
        List<Integer> values = new ArrayList<Integer>(counterProducts.values());

        int maxValue = 0;
        for (int i = 0; i < values.size(); i++){
            if (maxValue < values.get(i)){
                maxValue = values.get(i);
            }
        }

        List<String> keys = new ArrayList<String>(counterProducts.keySet());

        while (maxValue > 0){
            for (int i = 0; i < keys.size(); i++){
                if (counterProducts.get(keys.get(i)) == maxValue){
                    counterProductsSorted.put(keys.get(i), maxValue);                   
                }
            }
            maxValue--;
        }
        System.out.println(counterProductsSorted);

    }

    

        

}

        
        
  
