
from .base import BaseCommand

import bodskit.replace_statement_identifiers


class Command(BaseCommand):
    name = 'replace-statement-identifiers'
    help = 'replaces all existing statement identifiers'

    def add_arguments(self):
        self.add_argument('statement_or_package_file', 
        	help='The file that contains the BODS package or statement')
        self.add_argument('output_file',
        	help='The file to output with new statement identifiers')

    def handle(self):
        rsi = bodskit.replace_statement_identifiers.ReplaceStatementIdentifiers(
        	input_filename=self.args.statement_or_package_file,
        	output_filename = self.args.output_file)
        rsi.handle()
