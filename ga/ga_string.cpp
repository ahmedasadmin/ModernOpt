// an individual will represent a string value with their corresponding fitness
#include <iostream>
#include <string>
#include <ctime>
#include <vector>
#include <algorithm>
#include <chrono>
#include <thread>

namespace details{
    std::string get_random_string(size_t length){
        const std::string charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        std::string result;
        for(size_t i=0; i<length; ++i){
            result +=charset[rand() % charset.size()];
        }
        return result;
    }
    // get_random number
    int get_random_number(int min, int max){
        return min + (rand() % (max - min + 1));
    }
    // get random character
    char get_random_char(){
        const std::string charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ";
        return charset[rand() % charset.size()];
    }

}
class Individual{
    public:
        // one cosntructor to initialize a random individual 
        // both constructors calculate the fitness right 
        // details::get_randon_string is the helper function which reates ()
        // a randon string, can you find the helper function in the example 
        Individual() : m_value(details::get_random_string(target.size())), m_fitness(0)
        {
            calculate_fitness();
        }
        // one constructor where we already have a string 
        Individual(const std::string& value) : m_value(value), m_fitness(0){
            calculate_fitness();
        }

        // some getters 
        std::string get_value() const{
            return m_value;
        }
        std::size_t get_fitness() const{
            return m_fitness;
        }
        // the square bracket overload to access single character 
        char operator[](const int i) const{
            return m_value[i];
        }
        // the greater operator overload to sort fitness 
        bool operator > (const Individual& rhs) const {
            return (m_fitness > rhs.m_fitness);
        }
    private:
        // the fitness is calculated here 
        // the more charaters match our targer the higher fitness
        void calculate_fitness(){
            for(int i = 0; i < target.size(); ++i){
                if (target[i]==m_value[i]){
                    m_fitness++;
                }
            }
        }
    private:
    std::string m_value;
    std::size_t m_fitness;
    public:
    static const std::string target;

};      
const std::string Individual::target = "Hello World";
Individual create_child(const Individual& mother, const Individual& father
    ,const std::size_t parent_ratio, const std::size_t mutate_probability)
{
    // initialize childs string value
    std::string childs_value{""};

    // iterate over all characters of the target size
    for (std::size_t i=0; i<Individual::target.size(); ++i){
        if (details::get_random_number(0, 100) < mutate_probability){
            childs_value += details::get_random_char();

            // else we either mothers or fathers characters

        }else if (details::get_random_number(0, 100) < parent_ratio){
            childs_value += mother[i];
        }else{
            childs_value += father[i];
        }
    }

    return Individual{childs_value};
} // end of create child function ...

class Population{

    public:
    // population cosntructors where we pass all values we need
    // all ratios and propbabilities are given in integer percentage values 0...100
    // and absolute value calculated here in the constructor
    Population( const std::size_t max_population,
                const std::size_t parent_ratio,
                const std::size_t mutate_probability,
                const std::size_t transfer_ratio, 
                const std::size_t crossover)
          : m_generation{1}, m_parent_ratio{parent_ratio},m_mutate_probability{mutate_probability}
          {
            m_transfer_count = (transfer_ratio*max_population)/100;
            m_crossover_threshold = (crossover*max_population)/100;

            // m_new_individuals_per_generation is the number of created individuals 
            // int next generation 
            m_new_individuals_per_generation = max_population-m_transfer_count;
            // reserve some storage for population 
            m_population.reserve(max_population);
            std::generate_n(std::back_inserter(m_population), max_population, [](){ return Individual{}; });
            this->sort();
        }    // end constructor-1
        std::size_t get_generation() const{
            return m_generation;
        }
        // just use std::sort to get decending order of indivituals 
        void sort(){
            std::sort(std::begin(m_population), std::end(m_population), [](const auto& left, const auto& right){return left > right;});
        }
        void create_next_generation(){
            // increment generation counter
            m_generation++;

            // create a tmp which represets the new generation 
            std::vector<Individual> next_generation;
            next_generation.reserve(m_population.size());
            for(std::size_t i = 0; i < m_transfer_count; ++i){
                next_generation.push_back(m_population[i]);
            }
            // create the crossover individuals 
            for(std::size_t i = 0; i < m_new_individuals_per_generation; ++i){
                // the mother is any individual between 0...m_crossover_threshold
                Individual& mother = this->m_population[details::get_random_number(0, m_crossover_threshold)];
                Individual& father = this->m_population[details::get_random_number(0, m_crossover_threshold)];
                // and push the new created child to the new generation 
                // the helper functions described below
                next_generation.push_back(create_child(mother, father, m_parent_ratio, m_mutate_probability));
            }

            m_population = next_generation;
        }
    
        const Individual& front() const {
            return m_population.front();
        }
    private:
        std::vector<Individual>m_population;
        std::size_t m_generation;
        std::size_t m_parent_ratio;
        std::size_t m_mutate_probability;
        std::size_t m_transfer_count;
        std::size_t m_crossover_threshold;
        std::size_t m_new_individuals_per_generation;
};


int main(){
    std::srand(static_cast<unsigned>(std::time(nullptr)));   // seed rand to ensure different outputs
    // variables we can adjust 
    const std::size_t population_size = 500;
    const std::size_t parent_ratio = 50;
    const std::size_t mutate_probability = 10;
    const std::size_t transfer_ratio = 15;
    const std::size_t crossover = 50;
    // create our population in the first generation
    Population population(population_size, parent_ratio, mutate_probability, transfer_ratio, crossover);


    // until we haven't found our target 
    // we continue to create a next generation and sort them
    while(population.front().get_fitness() < Individual::target.size()) 
    {
        std::cout <<"[INFO] Generation " << population.get_generation() 
        << " | Generations best match: " << population.front().get_value() 
        <<" | Fitness: " << population.front().get_fitness() << "\r";
        std::cout.flush();
        population.create_next_generation(); 
        population.sort();
            // Sleep for better visualization (simulates a progress effect)
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    std::cout << "[DONE] Evolution Complete! Best match found after " 
    << population.get_generation() << " generations: " 
    << population.front().get_value() << "\n";
   
    return EXIT_SUCCESS;
}
