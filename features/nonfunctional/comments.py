#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature


class CommentsFeature(Feature):

    def id():
        return 'nonfunctional.comments'

    def category():
        return 'Non-Functional'

    def title():
        return 'Comments'

    def desc():
        return 'Start comments with a # by default'

    def dependencies():
        return []

    def default_options():
        return {
            'Symbol': '#'
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('comment', CommentsFeature.parse_comment)
        
        calculator.feature_options['nonfunctional.comments'] = cls.default_options()

    def parse_comment(self, expr, i, items, flags):
        next = expr[i:]
        if next[0] == self.feature_options['nonfunctional.comments']['Symbol']:
            i = next.find("\n")
            if i == -1:
                i = len(next)
            return [CommentItem(next[0:i])], i, None
        return None, None, None


class CommentItem(NonFunctionalItem):

	def desc(self):
		return 'comment'
