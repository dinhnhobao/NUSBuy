'''
from django.test import TestCase
from budget.models import Project, Category, Expense

class TestModels(TestCase):
    def setUp(self): #run before all other test methods
        #setup a certain scenario
        self.project1 = Project.objects.create(
            name = 'Project 1', #slug is already slugnified, the slug is also the name
            budget = 10000
        )

    #check the slugify method in save in Project
    def test_project_is_assigned_slug_on_creation(self): 
        self.assertEquals(self.project1.slug, 'project-1')

    #check the budget_left property in Project
    def test_budget_left(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        #create two expenses
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense2',
            amount = 2000,
            category = category1
        )

        #expect a budget of 7000
        self.assertEquals(self.project1.budget_left, 7000)

    #check the number of total_transaction property in Project
    def test_project_total_transactions(self):
        project2 = Project.objects.create(
            name = 'project2',
            budget = 10000
        )

        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        category2 = Category.objects.create(
            project = project2,
            name = 'development'
        )

        #create two expenses
        Expense.objects.create(
            project = self.project1, #this expense is for project 1
            title = 'expense1',
            amount = 1000,
            category = category1
        )

        Expense.objects.create(
            project = project2, #1st expense for project 2
            title = 'expense2',
            amount = 2000,
            category = category2
        )

        Expense.objects.create(
            project = project2, #2nd expense for project 2
            title = 'expense2',
            amount = 3000,
            category = category2
        )
        self.assertEquals(self.project1.total_transactions, 1)
        self.assertEquals(project2.total_transactions, 2)


'''
Project: (name, slug/id, budget)
Category: (Project, categoryName)
Expense: (project, title, amount, category)
'''