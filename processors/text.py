import tiktoken
import openai
import config

class TextProcessor:
    """
    A class responsible for processing text data, including decoding, tokenizing,
    and summarizing text using the OpenAI API.
    """

    def __init__(self, model="gpt-4", max_tokens=100000):
        """
        Initializes the TextProcessor with a specific model and max token limit.

        :param model: The OpenAI model to use (default: "gpt-4").
        :param max_tokens: The maximum number of tokens to use in text processing (default: 10000).
        """
        self.encoding = tiktoken.encoding_for_model(model)
        self.max_tokens = max_tokens
        config.app_logger.info("TextProcessor initialized.")

    def decode_text(self, pdf_data):
        """
        Decodes binary PDF data to text using utf-8 or latin-1 encoding.

        :param pdf_data: The binary data from a PDF file.
        :return: The decoded text as a string.
        """
        config.app_logger.debug("Decoding text from PDF data...")
        try:
            return pdf_data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return pdf_data.decode('latin-1')
            except UnicodeDecodeError:
                config.app_logger.warning("Failed to decode PDF data with both utf-8 and latin-1. Skipping...")
                return ''

    def split_text_by_tokens(self, text):
        """
        Splits the text into chunks based on a maximum token count.

        :param text: The full text to split.
        :return: A list of text chunks, each within the max token limit.
        """
        tokens = self.encoding.encode(text)
        chunks = []

        for i in range(0, len(tokens), self.max_tokens):
            chunk = tokens[i:i + self.max_tokens]
            chunk_text = self.encoding.decode(chunk)
            chunks.append(chunk_text)

        config.app_logger.info(f"Text split into {len(chunks)} chunks.")
        return chunks

    def summarize_text(self, input_text, system_message):
        """
        Summarizes the given text using the OpenAI API.

        :param input_text: The text to summarize.
        :param system_message: The system message or prompt to guide the summarization.
        :return: The summarized text.
        """
        config.app_logger.info("Summarizing text using OpenAI API...")

        try:
            response = openai.ChatCompletion.create(
                engine="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=3000
            )
            return response['choices'][0]['message']['content']

        except openai.error.InvalidRequestError as e:
            config.app_logger.error(f"OpenAI API request failed: {str(e)}")
            return "Error: The request contained repetitive patterns. Please modify the input and try again."

        except Exception as e:
            config.app_logger.error(f"An unexpected error occurred: {str(e)}")
            return "Error: An unexpected issue occurred. Please try again later."

    def summarize_chunks(self, chunks, system_message):
        """
        Summarizes a list of text chunks and returns a list of summaries.

        :param chunks: A list of text chunks to summarize.
        :param system_message: The system message or prompt to guide the summarization.
        :return: A list of summary strings.
        """
        summaries = []
        for chunk in chunks:
            summary = self.summarize_text(chunk, system_message)
            summaries.append(summary)
        config.app_logger.info(f"Summarized {len(summaries)} chunks.")
        return summaries

    def combine_summaries(self, summaries):
        """
        Combines a list of summary chunks into a single, cohesive summary.

        :param summaries: A list of summary strings to combine.
        :return: A single string representing the combined summary.
        """
        combined_summary = "\n\n".join(summaries)
        config.app_logger.info("Combined summaries into a final summary.")
        return combined_summary
