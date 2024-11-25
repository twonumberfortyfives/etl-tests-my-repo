# Preliminary Task: Junior Test Engineer

Hello! Following your advice about the need for data validation, I implemented the DataFrame validation library we discussed on the phone. To maintain the general style of the ETL process you wrote, I created an additional class for data validation without changing the core logic. This made the code more modular and easy to extend.

I also made sure not to modify the original code that needed testing. This was intentional to preserve its authenticity and ensure the tests reflect a real-world scenario. By testing the original unaltered code, I can demonstrate how the validation module integrates seamlessly without requiring any changes, highlighting its adaptability and compatibility. This approach also ensures the testing process is as close as possible to how it would function in a production environment.

## How I implemented the tests
I decided to run the tests via Docker because I encountered several issues:

- difficulties with imports,
- incompatibilities between versions,
- and the desire to simplify the launch process for you.

Now, you can run all tests with a single command:  
```bash
docker-compose up --build
```
This makes the verification process stable and independent of your local environment.
In the project, I used both unittest and pytest to demonstrate my ability to work with different testing frameworks. I chose unittest for classic structured tests, and pytest for checking in a more modern style, given its flexibility and wide capabilities.

## Thank you for your attention! 😊
I hope you like the result. It was a great task and I tried my best to show my skills. I will be glad to show more of my capabilities in the future!
