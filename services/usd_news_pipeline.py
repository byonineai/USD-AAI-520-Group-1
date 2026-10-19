class USDNewsPipeline:
    """
    Executes the news-processing stages in sequence.

    Each stage receives the output produced by the previous
    stage and returns the updated shared context.
    """

    def __init__(
        self,
        stages
    ):
        self.stages = stages

    def run(
        self,
        data
    ) -> dict:

        all_current_data = data

        for stage in self.stages:

            all_current_data = stage.process(
                all_current_data
            )

        return all_current_data