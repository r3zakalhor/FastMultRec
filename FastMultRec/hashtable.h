#ifndef HASH_CLASS
#define HASH_CLASS

#include <string>
#include <iostream>
#include <vector>
#include <list>
#include "node.h"
#include "util.h"
#include "newicklex.h"
#include "node.h"
#include "genespeciestreeutil.h"
#include "treeiterator.h"

using namespace std;


/*struct cell
{
    list<Node*> node;
    int dupheight;

    cell(Node* n) {
        node.push_back(n);
    }
    /*void removenode(string label) {
        for (int i = 0; i < node.size(); i++) {
            if (node[i]->GetLabel() == label) {
                node.erase(node.begin() + i);
            }
        }
    }

    void print() {
        for (int i = 0; i < node.size(); i++) {
            cout << node[i]->GetLabel() << ", ";

        }
        cout << endl;
    }
};*/

class hashlist
{
private:
    //vector< vector<Node *> > listofheights;
    vector< unordered_set<Node*> > listofheights;
public:

    hashlist()
    {
        listofheights.resize(1);
    }
    int size() {
        if (listofheights.size() > 0)
            return listofheights.size() - 1;
        else
            return 0;
    }
    
    unordered_set<Node*> return_max_heights() {
        if (listofheights.size() > 0)
            return listofheights[listofheights.size() - 1];
        else
            return unordered_set<Node*>();
    }

    bool is_unique_max(Node* g) {
        if (listofheights.size() > 0) {
            int size = listofheights.size() - 1;
            if (listofheights[size].size() == 1) {
                unordered_set<Node*>::iterator itr;
                for (itr = listofheights[size].begin(); itr != listofheights[size].end(); itr++)
                    if ((*itr)->GetIndex() == g->GetIndex()) {
                        return true;
                    }
            }
        }
        return false;
    }



    bool is_unique_after_max(Node* g) {
        if (listofheights.size() >= 2) {
            int size = listofheights.size() - 2;
            if (listofheights[size].size() == 1) {
                unordered_set<Node*>::iterator itr;
                for (itr = listofheights[size].begin(); itr != listofheights[size].end(); itr++)
                    if ((*itr) == g) {
                        return true;
                    }
            }
        }
        return false;
    }





    bool is_unique_element(Node* g, int height) {
        if (listofheights[height].size() == 1) {
            unordered_set<Node*>::iterator itr;
            for (itr = listofheights[height].begin(); itr != listofheights[height].end(); itr++)
                if ((*itr)->GetIndex() == g->GetIndex()) {
                    //cout << "indwex: " << g->GetIndex() << endl;
                    return true;
                }
        }
        return false;
    }


    int dupheight_at_subtree(Node* g) {
        if (listofheights.size() <= 1) {
            return 0;
        }
        else {
            for (int i = 1; i < listofheights.size(); i++) {
                //cout << " dup heights of " << i << " are : ";
                /*auto it = std::next(listofheights.begin(), i);
                for (int j = 0; j < listofheights[i].size(); j++) {
                //for (std::list<Node*>::iterator it = listofheights[i].begin(); it != listofheights[i].end(); ++it) {
                    //std::cout << *it << ' '; // You can access elements calling the operator[] , you need an iterator.
                    cout << it->operator [](j)->GetLabel() << ", ";
                    //cout << listofheights[i][j].liGetLabel() << ", "; // You can access elements calling the operator[] , you need an iterator.
                }*/
                unordered_set<Node*>::iterator itr;
                for (itr = listofheights[i].begin(); itr != listofheights[i].end(); itr++)
                    if ((*itr) == g)
                        return i;
            }
        }
        return 0;
    }

    void add_cell(int newdupheight, Node* g)
    {
        //cout << "glabel : " << g << "  dup height : " << newdupheight << endl;
        //list<int> l;
        //l.push_back(g);
        //listofheights.push_back(g);
        //Node *c = new Node();
        //listofheights.push_back(c);
        int previoussize = listofheights.size() - 1;
        if (newdupheight > previoussize) {
           int newsize = newdupheight + 1;
           //cout << "previous size " << previoussize << " newsize " << newsize << endl;
           listofheights.resize(newsize);
        }
        listofheights[newdupheight].insert(g);

    }

    bool remove(int dupheight, Node* g)
    {
        if (dupheight < listofheights.size()) {
            //auto it = std::next(listofheights.begin(), dupheight);
            /*unordered_set<Node*>::iterator itr;
            //for (int j = 0; j < listofheights[dupheight].size(); j++) {
            for (itr = listofheights[dupheight].begin(); itr != listofheights[dupheight].end(); itr++){
                //if (it->operator [](j)->GetLabel() == nodelabel) {
                if ((*itr)->GetLabel() == g->GetLabel()) {
                    listofheights[dupheight].erase(listofheights[dupheight].begin() + j);
                    if (dupheight == listofheights.size() - 1 && listofheights[dupheight].empty()) {
                        int newsize = dupheight;
                        listofheights.resize(newsize);
                    }
                    return true;
                }
            }*/
            listofheights[dupheight].erase(g);
            if (dupheight == listofheights.size() - 1 && listofheights[dupheight].empty()) {
                int newsize = dupheight;
                listofheights.resize(newsize);
            }
            return true;
        }
        //listofheights[dupheight].erase(g);
        return false;
    }

    void print() {
        if (listofheights.size() == 0) {
            cout << " is empty " << endl;
        }
        else {
            for (int i = 1; i < listofheights.size(); i++) {
                cout << " dup heights of " << i << " are : ";
                /*auto it = std::next(listofheights.begin(), i);
                for (int j = 0; j < listofheights[i].size(); j++) {
                //for (std::list<Node*>::iterator it = listofheights[i].begin(); it != listofheights[i].end(); ++it) {
                    //std::cout << *it << ' '; // You can access elements calling the operator[] , you need an iterator.
                    cout << it->operator [](j)->GetLabel() << ", ";
                    //cout << listofheights[i][j].liGetLabel() << ", "; // You can access elements calling the operator[] , you need an iterator.
                }*/
                bool has_one = false;
                unordered_set<Node *>::iterator itr;
                for (itr = listofheights[i].begin(); itr != listofheights[i].end(); itr++) {
                    cout << (*itr)->GetLabel() << ", ";
                    has_one = true;
                }
                if (has_one)
                    cout << "          " << endl;
            }
        }
        //cout << endl;
    }
};

#endif // HASH_CLASS
