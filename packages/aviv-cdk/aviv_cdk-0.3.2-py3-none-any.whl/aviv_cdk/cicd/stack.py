import typing
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ssm,
    aws_codebuild,
    pipelines
)
from . import (
    sources as gh_sources
)

class CodePipelineStack(Stack):
    __connections: dict={}
    __sources: dict={}
    pipeline: pipelines.CodePipeline
    step: pipelines.ShellStep
    source: pipelines.CodePipelineSource

    def __init__(
            self, scope: Construct, construct_id: str, *,
            connections: dict=None,
            self_pipeline: bool=True,
            repository: typing.Union[str, gh_sources.SourceRepositoryAttrs]=None,
            code_build_clone_output: bool=True,
            trigger_on_push: bool=None,
            shellstep: typing.Union[dict, pipelines.ShellStepProps]={},
            codepipeline: typing.Union[dict, pipelines.CodePipelineProps]={},
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if connections:
            self.connections = connections

        if self_pipeline:
            if not 'input' in shellstep:
                if not repository:
                    info = gh_sources.git_repository_info()
                    repository = f"{info.get('url')}@{info.get('branch')}"
                shellstep['input'] = self.add_source(repository=repository, code_build_clone_output=code_build_clone_output, trigger_on_push=trigger_on_push)
            self.step = self.shellstep(**shellstep)
            self.pipeline = self.codepipeline(step=self.step, **codepipeline)

    def shellstep(self, **shellstep) -> pipelines.ShellStep:
        if not 'commands' in shellstep:
            shellstep['commands'] = [
                "npm install -g aws-cdk",
                "python -m pip install aws-cdk-lib aviv-cdk",
                "cdk synth"
            ]
        return pipelines.ShellStep("Synth", **shellstep)

    def codepipeline(self, step: pipelines.ShellStep, **cpattr) -> pipelines.CodePipeline:
        return pipelines.CodePipeline(
            self, "Pipeline",
            synth=step,
            **cpattr
        )

    def add_source(self, repository: typing.Union[str, gh_sources.SourceRepositoryAttrs], code_build_clone_output: bool=None, trigger_on_push: bool=None) -> pipelines.CodePipelineSource:
        if isinstance(repository, str):
            repository = gh_sources.git_url_split(repository)
        sname = f"{repository['owner']}/{repository['repo']}"
        self.sources[sname] = pipelines.CodePipelineSource.connection(
            repo_string=sname,
            branch=repository['branch'],
            connection_arn=self.connections[repository['owner']],
            code_build_clone_output=code_build_clone_output,
            trigger_on_push=trigger_on_push
        )
        return self.sources[sname]

    @property
    def sources(self) -> dict:
        return self.__sources

    @sources.setter
    def sources(self, sources: dict) -> None:
        for name, url in sources.items():
            self.__sources[name] = url

    @property
    def connections(self) -> dict:
        return self.__connections

    @connections.setter
    def connections(self, connections: dict) -> None:
        for cname, connection_arn in connections.items():
            if connection_arn.startswith('aws:ssm:'):
                connection_arn = aws_ssm.StringParameter.value_from_lookup(
                    self, parameter_name=connection_arn.replace('aws:ssm:', '')
                )
            self.__connections[cname] = connection_arn
