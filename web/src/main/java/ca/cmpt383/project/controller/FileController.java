package ca.cmpt383.project.controller;

import ca.cmpt383.project.model.ClassificationResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@RestController
public class FileController {
    private static final int HTTP_OK = 200;
    private static final int HTTP_ERROR = 400;

    @PostMapping("/upload")
    public List<ClassificationResult> upload(@RequestParam("file") MultipartFile file, HttpServletResponse response) {
        // System.out.println("file name : " + file.getOriginalFilename());
        // System.out.println("file size : " + file.getSize());

        Path filepath = Paths.get("/tensor", "image.jpg");

        // adapted from https://stackoverflow.com/questions/24339990/how-to-convert-a-multipart-file-to-file/39572293
        try (OutputStream os = Files.newOutputStream(filepath)) {
            os.write(file.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }

        List<ClassificationResult> ClassificationResults = new ArrayList<>();

        try {
            // adapted from https://www.baeldung.com/java-working-with-python
            String[] command = new String[] {"python3", "image_classification.py"};
            ProcessBuilder pb = new ProcessBuilder().directory(new File("/tensor")).command(command);
            Process process =  pb.start();

            // ignore process error or output
            process.getErrorStream().close();
            process.getOutputStream().close();

            InputStreamReader inputStreamReader = new InputStreamReader(process.getInputStream());
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            StringBuilder stringBuilder = new StringBuilder();
            String resultString;

            int count=1;
            while ((resultString = bufferedReader.readLine()) != null) {
                stringBuilder.append(resultString).append("\n");
                ClassificationResults.add(new ClassificationResult(count++, resultString));
            }
            response.setStatus(HTTP_OK);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            response.setStatus(HTTP_ERROR);
        }

        return ClassificationResults;
    }
}
